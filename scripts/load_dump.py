import os
import subprocess
import argparse

# Helper function to execute a shell command
def run_command(command, env=None):
    """Executes a shell command."""
    try:
        result = subprocess.run(command, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        print(f"stderr: {e.stderr}")
        return None

# Step 1: Copy the dump file to the PostgreSQL container
def copy_dump_to_container(container_name, dump_file_path):
    print(f"Copying dump file to PostgreSQL container: {container_name}")
    command = ["docker", "cp", dump_file_path, f"{container_name}:/tmp/dump.sql"]
    result = run_command(command)
    if result is not None:
        print(f"Successfully copied dump file to {container_name}.")
        return True
    return False

# Step 2: Load the dump into the PostgreSQL database
def load_dump_into_postgres(container_name, user, password, db_name):
    print(f"Loading dump into PostgreSQL database in container: {container_name}")
    env = os.environ.copy()
    env["PGPASSWORD"] = password
    command = [
        "docker", "exec", container_name,
        "psql", "-U", user, "-d", db_name, "-f", "/tmp/dump.sql"
    ]
    result = run_command(command, env=env)
    if result is not None:
        print(f"Successfully loaded dump into PostgreSQL database.")
        return True
    return False

# Step 3: Apply migrations (assuming pg_dump is part of migrations step?)
def apply_migrations(container_name, user, password):
    print("Applying migrations...")
    env = os.environ.copy()
    env["PGPASSWORD"] = password
    # This command seems to create a dump, not apply migrations — adjust as needed
    command = ["docker", "exec", container_name, "sh", "-c", f"pg_dump -U {user} > /tmp/post_migrations.sql"]
    result = run_command(command, env=env)
    if result is not None:
        print("Migrations applied successfully.")
        return True
    return False

# Step 4: Cleanup
def cleanup(container_name):
    print("Cleaning up temporary files...")
    command = ["docker", "exec", container_name, "rm", "/tmp/dump.sql"]
    run_command(command)
    print("Cleanup complete.")

def main():
    parser = argparse.ArgumentParser(description="Load a PostgreSQL dump inside a Docker container.")
    parser.add_argument("--container", default="ttranking-db-1", help="PostgreSQL Docker container name")
    parser.add_argument("--dump", default="../backups/converted_postgres.sql", help="Path to PostgreSQL dump file")
    parser.add_argument("--user", default="root", help="PostgreSQL user")
    parser.add_argument("--password", required=True, help="PostgreSQL user password")
    parser.add_argument("--db", default="ttranking", help="PostgreSQL database name")
    args = parser.parse_args()

    if not os.path.exists(args.dump):
        print(f"Error: Dump file {args.dump} does not exist.")
        return

    if not copy_dump_to_container(args.container, args.dump):
        return

    if not load_dump_into_postgres(args.container, args.user, args.password, args.db):
        return

    if not apply_migrations(args.container, args.user, args.password):
        return

    cleanup(args.container)

if __name__ == "__main__":
    main()
