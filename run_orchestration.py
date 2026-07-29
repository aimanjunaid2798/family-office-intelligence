from app.discovery.orchestrator import DiscoveryOrchestrator

if __name__ == "__main__":
    orchestrator = DiscoveryOrchestrator(
        input_csv="datasets/raw/discovered_family_offices.csv", 
        output_csv="datasets/processed/verified_family_offices.csv"
    )
    orchestrator.run()