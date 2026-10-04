"""
ALGOX — SQLite Database Layer
Persistent storage for empirical benchmark runs, saved experiments, generated datasets, and system configuration.
"""
from typing import List, Dict, Any, Optional
import sqlite3
import os
import json
import csv
import io
from datetime import datetime

DEFAULT_DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'algox.db')

DEFAULT_SETTINGS = {
    'default_dataset_size': '500',
    'default_repetitions': '3',
    'max_safe_n_quadratic': '5000',
    'visualizer_array_size': '25',
    'animation_speed_ms': '50',
    'animations_enabled': 'true',
    'theme': 'dark'
}

class AlgoxDB:
    def __init__(self, db_path: str = DEFAULT_DB_PATH):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.init_db()

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        """Initializes tables and default settings if not existing."""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Experiments table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS experiments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    algorithm TEXT NOT NULL,
                    category TEXT NOT NULL,
                    dataset TEXT NOT NULL,
                    input_size INTEGER NOT NULL,
                    avg_time REAL NOT NULL,
                    min_time REAL NOT NULL,
                    max_time REAL NOT NULL,
                    std_dev REAL DEFAULT 0.0,
                    seed INTEGER DEFAULT 42,
                    comparisons INTEGER NOT NULL,
                    swaps INTEGER NOT NULL,
                    memory_bytes INTEGER NOT NULL,
                    correct INTEGER NOT NULL,
                    repetitions INTEGER NOT NULL,
                    notes TEXT
                )
            ''')

            # Migration check: ensure std_dev and seed exist on existing table
            cursor.execute("PRAGMA table_info(experiments)")
            existing_cols = {row['name'] for row in cursor.fetchall()}
            if 'std_dev' not in existing_cols:
                cursor.execute("ALTER TABLE experiments ADD COLUMN std_dev REAL DEFAULT 0.0")
            if 'seed' not in existing_cols:
                cursor.execute("ALTER TABLE experiments ADD COLUMN seed INTEGER DEFAULT 42")

            # Saved experiments table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS saved_experiments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    experiment_id INTEGER,
                    title TEXT NOT NULL,
                    notes TEXT,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY(experiment_id) REFERENCES experiments(id) ON DELETE CASCADE
                )
            ''')

            # Datasets table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS datasets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    distribution TEXT NOT NULL,
                    size INTEGER NOT NULL,
                    seed INTEGER,
                    created_at TEXT NOT NULL
                )
            ''')

            # Settings table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            ''')

            # Counters table (for recommendations count etc.)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS counters (
                    name TEXT PRIMARY KEY,
                    count INTEGER NOT NULL DEFAULT 0
                )
            ''')

            # Seed default settings if empty
            for k, v in DEFAULT_SETTINGS.items():
                cursor.execute(
                    'INSERT OR IGNORE INTO settings (key, value, updated_at) VALUES (?, ?, ?)',
                    (k, v, datetime.now().isoformat())
                )

            # Seed recommendations counter
            cursor.execute(
                'INSERT OR IGNORE INTO counters (name, count) VALUES (?, ?)',
                ('recommendations_generated', 0)
            )

            conn.commit()

    # --- EXPERIMENTS CRUD ---
    def insert_experiment(self, data: Dict[str, Any]) -> int:
        timestamp = data.get('timestamp', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO experiments (
                    timestamp, algorithm, category, dataset, input_size,
                    avg_time, min_time, max_time, std_dev, seed, comparisons, swaps,
                    memory_bytes, correct, repetitions, notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                timestamp,
                data['algorithm'],
                data.get('category', 'Sorting'),
                data.get('dataset', 'Random'),
                int(data['input_size']),
                float(data['avg_time']),
                float(data['min_time']),
                float(data['max_time']),
                float(data.get('std_dev', 0.0)),
                int(data['seed']) if data.get('seed') is not None else 42,
                int(data['comparisons']),
                int(data['swaps']),
                int(data.get('memory_bytes', 64)),
                1 if data.get('correct', True) else 0,
                int(data.get('repetitions', 1)),
                data.get('notes', '')
            ))
            conn.commit()
            return cursor.lastrowid

    def get_experiments(
        self,
        limit: int = 100,
        algorithm: Optional[str] = None,
        category: Optional[str] = None,
        distribution: Optional[str] = None,
        search: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        query = 'SELECT * FROM experiments WHERE 1=1'
        params = []

        if algorithm and algorithm != 'All':
            query += ' AND algorithm = ?'
            params.append(algorithm)
        if category and category != 'All':
            query += ' AND category = ?'
            params.append(category)
        if distribution and distribution != 'All':
            query += ' AND dataset = ?'
            params.append(distribution)
        if search:
            query += ' AND (algorithm LIKE ? OR notes LIKE ? OR dataset LIKE ?)'
            search_param = f'%{search}%'
            params.extend([search_param, search_param, search_param])

        query += ' ORDER BY id DESC LIMIT ?'
        params.append(limit)

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def get_experiment_by_id(self, exp_id: int) -> Optional[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM experiments WHERE id = ?', (exp_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def get_experiment_count(self) -> int:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM experiments')
            return cursor.fetchone()[0]

    def get_validated_experiment_count(self) -> int:
        """Returns the total number of verified and correct experiments."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM experiments WHERE correct = 1')
            return cursor.fetchone()[0]

    def get_fastest_algorithm(self, category: Optional[str] = 'Sorting') -> Optional[Dict[str, Any]]:
        """Returns the fastest algorithm within a specific category (default Sorting) based on normalized time per element."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if category and category != 'All':
                cursor.execute('''
                    SELECT algorithm, category, AVG(avg_time) as avg_time,
                           AVG(avg_time / MAX(input_size, 1)) as normalized_time, COUNT(*) as runs
                    FROM experiments
                    WHERE category = ?
                    GROUP BY algorithm
                    ORDER BY normalized_time ASC
                    LIMIT 1
                ''', (category,))
            else:
                cursor.execute('''
                    SELECT algorithm, category, AVG(avg_time) as avg_time,
                           AVG(avg_time / MAX(input_size, 1)) as normalized_time, COUNT(*) as runs
                    FROM experiments
                    GROUP BY algorithm
                    ORDER BY normalized_time ASC
                    LIMIT 1
                ''')
            row = cursor.fetchone()
            return dict(row) if row else None

    def get_domain_fastest_algorithms(self) -> Dict[str, Optional[Dict[str, Any]]]:
        """Separates performance by domain: Sorting, Searching, Graph."""
        return {
            'Sorting': self.get_fastest_algorithm('Sorting'),
            'Searching': self.get_fastest_algorithm('Searching'),
            'Graph': self.get_fastest_algorithm('Graph')
        }

    def ensure_performance_matrix(self):
        """
        Ensures that real empirical benchmark measurements exist for all 30 combinations
        (6 sorting algorithms x 5 dataset distributions). Generates and logs any missing combinations.
        """
        from core.benchmark import run_benchmark
        from core.dataset import generate_dataset, DISTRIBUTIONS
        
        sorting_algos = ['Bubble Sort', 'Selection Sort', 'Insertion Sort', 'Merge Sort', 'Quick Sort', 'Heap Sort']
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT DISTINCT algorithm, dataset FROM experiments WHERE category = "Sorting"')
            existing = {(r['algorithm'], r['dataset']) for r in cursor.fetchall()}

        for dist in DISTRIBUTIONS:
            # Generate dataset once per distribution with fixed reproducible seed
            raw_arr = generate_dataset(500, dist, seed=42)
            for algo in sorting_algos:
                if (algo, dist) not in existing:
                    # Run real benchmark
                    res = run_benchmark(algo, raw_arr, repetitions=3)
                    self.insert_experiment({
                        'algorithm': algo,
                        'category': 'Sorting',
                        'dataset': dist,
                        'input_size': 500,
                        'avg_time': res['avg_time'],
                        'min_time': res['min_time'],
                        'max_time': res['max_time'],
                        'std_dev': res.get('std_dev', 0.0),
                        'seed': 42,
                        'comparisons': res['comparisons'],
                        'swaps': res.get('swaps', 0) + res.get('shifts', 0),
                        'memory_bytes': res.get('memory_bytes', 64),
                        'correct': 1 if res['correct'] else 0,
                        'repetitions': 3,
                        'notes': f'Empirical Baseline Matrix ({dist}, N=500, seed=42)'
                    })
                    existing.add((algo, dist))

    def get_average_execution_time(self) -> Optional[float]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT AVG(avg_time) FROM experiments')
            val = cursor.fetchone()[0]
            return float(val) if val is not None else None

    def get_recent_experiments(self, limit: int = 10) -> List[Dict[str, Any]]:
        return self.get_experiments(limit=limit)

    def delete_experiment(self, exp_id: int):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM experiments WHERE id = ?', (exp_id,))
            cursor.execute('DELETE FROM saved_experiments WHERE experiment_id = ?', (exp_id,))
            conn.commit()

    def clear_history(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM experiments')
            cursor.execute('DELETE FROM saved_experiments')
            conn.commit()

    # --- SAVED EXPERIMENTS ---
    def save_experiment(self, experiment_id: Optional[int], title: str, notes: str) -> int:
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO saved_experiments (experiment_id, title, notes, created_at)
                VALUES (?, ?, ?, ?)
            ''', (experiment_id, title, notes, created_at))
            conn.commit()
            return cursor.lastrowid

    def get_saved_experiments(self) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT s.id as saved_id, s.experiment_id, s.title, s.notes as saved_notes, s.created_at,
                       e.*
                FROM saved_experiments s
                LEFT JOIN experiments e ON s.experiment_id = e.id
                ORDER BY s.id DESC
            ''')
            return [dict(row) for row in cursor.fetchall()]

    def delete_saved_experiment(self, saved_id: int):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM saved_experiments WHERE id = ?', (saved_id,))
            conn.commit()

    # --- DATASETS ---
    def log_dataset(self, name: str, distribution: str, size: int, seed: Optional[int] = None) -> int:
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO datasets (name, distribution, size, seed, created_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (name, distribution, size, seed, created_at))
            conn.commit()
            return cursor.lastrowid

    def get_dataset_count(self) -> int:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM datasets')
            return cursor.fetchone()[0]

    def get_recent_datasets(self, limit: int = 10) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM datasets ORDER BY id DESC LIMIT ?', (limit,))
            return [dict(row) for row in cursor.fetchall()]

    # --- SETTINGS ---
    def get_setting(self, key: str, default: Any = None) -> Any:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT value FROM settings WHERE key = ?', (key,))
            row = cursor.fetchone()
            return row['value'] if row else default

    def set_setting(self, key: str, value: Any):
        updated_at = datetime.now().isoformat()
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO settings (key, value, updated_at) VALUES (?, ?, ?)
                ON CONFLICT(key) DO UPDATE SET value = excluded.value, updated_at = excluded.updated_at
            ''', (key, str(value), updated_at))
            conn.commit()

    def get_all_settings(self) -> Dict[str, str]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT key, value FROM settings')
            return {row['key']: row['value'] for row in cursor.fetchall()}

    def reset_settings(self):
        updated_at = datetime.now().isoformat()
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM settings')
            for k, v in DEFAULT_SETTINGS.items():
                cursor.execute(
                    'INSERT INTO settings (key, value, updated_at) VALUES (?, ?, ?)',
                    (k, v, updated_at)
                )
            conn.commit()

    # --- RECOMMENDATION COUNTER ---
    def get_recommendations_count(self) -> int:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT count FROM counters WHERE name = ?', ('recommendations_generated',))
            row = cursor.fetchone()
            return row['count'] if row else 0

    def increment_recommendations_count(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE counters SET count = count + 1 WHERE name = ?
            ''', ('recommendations_generated',))
            conn.commit()

    # --- CSV EXPORT ---
    def export_experiments_csv(self) -> str:
        experiments = self.get_experiments(limit=10000)
        if not experiments:
            return ""

        output = io.StringIO()
        fieldnames = list(experiments[0].keys())
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(experiments)
        return output.getvalue()
