import csv
import logging
import os
from app.validation.strict_processor import StrictEntityValidator

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    input_file = 'datasets/processed/final_clean_evaluation.csv'
    output_file = 'datasets/validated/final_clean_evaluation_v2.csv'
    
    if not os.path.exists(input_file):
        logging.error(f"Execution Error: Target file '{input_file}' not found. Pipeline aborted.")
        return

    logging.info(f"Balanced Refinement Workflow Activated. Processing target: {input_file}")
    
    validator = StrictEntityValidator()
    
    with open(input_file, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames) if reader.fieldnames else []
        rows = list(reader)

    for col in ['final_status', 'final_score', 'validation_notes']:
        if col not in fieldnames:
            fieldnames.append(col)

    verified_count = 0
    rejected_count = 0

    for row in rows:
        name = row.get('name', '')
        current_status = row.get('final_status', 'Rejected')
        current_score = row.get('final_score', '0.0')
        current_notes = row.get('validation_notes', '')

        status, score, notes = validator.process_single_row(
            name=name,
            current_status=current_status,
            current_score=current_score,
            current_notes=current_notes
        )
        
        row['final_status'] = status
        row['final_score'] = score
        row['validation_notes'] = notes

        if status == 'Verified':
            verified_count += 1
        else:
            rejected_count += 1

    with open(output_file, mode='w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    logging.info("=" * 60)
    logging.info("SUCCESS: Balanced Refinement Execution Complete!")
    logging.info(f"-> Total Real Verified SFOs Recovered: {verified_count}")
    logging.info(f"-> Total Structural Noise/Garbage Filtered: {rejected_count}")
    logging.info(f"-> Saved Balanced Target Database to: {output_file}")
    logging.info("=" * 60)

if __name__ == '__main__':
    main()