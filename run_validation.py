from app.validation.post_process import AssessmentPipelineProcessor

if __name__ == "__main__":
    print("=" * 80)
    print("Running Final Autonomous Validation")
    print("=" * 80)
    
    processor = AssessmentPipelineProcessor(
        input_csv_path="datasets/processed/verified_family_offices.csv", 
        output_csv_path="datasets/processed/final_clean_evaluation.csv"
    )
    processor.run()