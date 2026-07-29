import logging
import subprocess
import sys

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_script(script_name):
    logging.info(f"Executing step pipeline script: {script_name}")
    try:
        result = subprocess.run(
            [sys.executable, script_name],
            check=True,
            text=True
        )
        logging.info(f"Successfully completed execution of: {script_name}")
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Pipeline Execution Failed inside script '{script_name}' with exit code {e.returncode}")
        return False

def main():
    pipeline_steps = [
        "run_discovery.py",
        "run_orchestration.py",
        "run_validation.py",
        "run_strict_processing.py"
    ]

    logging.info("=" * 60)
    logging.info("STARTING AUTOMATED END-TO-END DATA PIPELINE")
    logging.info("=" * 60)

    for step in pipeline_steps:
        success = run_script(step)
        if not success:
            logging.error("Pipeline chain interrupted due to a critical step failure. Process aborted.")
            sys.exit(1)

    logging.info("=" * 60)
    logging.info("SUCCESS: Entire Sequence Chain Pipeline Completed Perfectly!")
    logging.info("=" * 60)

if __name__ == "__main__":
    main()