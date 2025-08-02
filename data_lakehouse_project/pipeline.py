import subprocess
import os
import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, "src")

def run_step(name, script_path):
    print(f"\n🚀 Executando etapa: {name} ...")
    start = datetime.datetime.now()
    
    try:
        subprocess.run(["python", script_path], check=True)
        print(f"✅ {name} concluída com sucesso! ({datetime.datetime.now() - start})")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro na etapa {name}: {e}")
        exit(1)

if __name__ == "__main__":
    print("🔄 Iniciando pipeline completo...\n")

    # Etapa Bronze - Ingestão
    run_step("Bronze (Ingestão Reddit)", os.path.join(SRC_DIR, "ingestion", "reddit_api.py"))

    # Etapa Silver - Processamento
    run_step("Silver (Transformação e Limpeza)", os.path.join(SRC_DIR, "processing", "silver_transform.py"))

    # Etapa Gold - Agregações e Visualizações
    run_step("Gold (Agregações e Visualizações)", os.path.join(SRC_DIR, "analytics", "gold_aggregations.py"))

    print("\n🎉 Pipeline finalizado com sucesso! Arquivos prontos em /data/gold")