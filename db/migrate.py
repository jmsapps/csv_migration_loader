import os
import importlib.util
import sys

MIGRATIONS_DIR = 'db/migrations'
CURRENT_FILE = os.path.join(MIGRATIONS_DIR, '.current')

# Makes modules importable within migration files
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def load_migrations():
    files = sorted(f for f in os.listdir(MIGRATIONS_DIR) if f.endswith('.py'))

    return files

def read_current():
    if not os.path.exists(CURRENT_FILE):
        return None

    with open(CURRENT_FILE) as f:
        return f.read().strip()

def write_current(filename):
    with open(CURRENT_FILE, 'w') as f:
        f.write(filename)

def run(direction):
    migrations = load_migrations()
    current = read_current()

    start = 0 if not current else migrations.index(current) + 1

    if direction == 'up':
        if len(migrations[start:]) == 0:
            print('No migrations to run.')

            return

        for migration in migrations[start:]:
            print(f"Applying {migration}...")

            run_migration(migration, 'up')
            write_current(migration)

            break  # apply one at a time

        if len(migrations[start:]) == 1:
            print('Successfully ran migration.')
        if len(migrations[start:]) > 1:
            print('Successfully ran migrations.')

    elif direction == 'down':
        if current:
            print(f"Reverting {current}...")

            run_migration(current, 'down')
            idx = migrations.index(current)
            prev = migrations[idx - 1] if idx > 0 else ''

            write_current(prev)

            print('Successfully ran down migration.')
        else:
            print("No migration to revert.")

def run_migration(filename, method):
    path = os.path.join(MIGRATIONS_DIR, filename)
    spec = importlib.util.spec_from_file_location("migration", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    getattr(module, method)()

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in ("up", "down"):
        print("Usage: python db/migrate.py [up|down]")
        sys.exit(1)

    run(sys.argv[1])
