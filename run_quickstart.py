from verbaterra.iclhf.model import ICLHFModel
from verbaterra.engines.vsion import simulate_block
from verbaterra.core.metrics import nlis, crm

def main():
    df = simulate_block(n=120, seed=7)
    df["NLIS"] = nlis(df); df["CRM"] = crm(df)
    print(ICLHFModel().fit(df).summary())

if __name__ == "__main__":
    main()
