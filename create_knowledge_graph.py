from biocypher import BioCypher, Resource
from collectri.adapters.collectri_adapter import CollectriAdapter

# ----------------------
# Step 1: Data download and cache
# ----------------------

bc = BioCypher()
collectri = Resource(
    name="collectri",
    url_s="https://rescued.omnipathdb.org/CollecTRI.csv",
    lifetime=0,  # CollecTRI is a static resource
)

paths = bc.download(collectri)

# ----------------------
# Optional: Inspect data
# ----------------------

import pandas as pd

df = pd.read_csv(paths[0])
print(df.head())
print(df.columns)

# ----------------------
# Step 2: Load and configure adapter
# ----------------------

adapter = CollectriAdapter(paths[0])

# ----------------------
# Optional: For prototyping, we can use the Pandas functionality
# ----------------------

bc.add(adapter.get_nodes())
bc.add(adapter.get_edges())
dfs = bc.to_df()
for name, df in dfs.items():
    print(name)
    print(df.head())

# ----------------------
# Step 3: Write nodes and edges, import call, and summarise the run
# ----------------------

bc = BioCypher()  # reset BioCypher, otherwise we would deduplicate from previous run
bc.write_nodes(adapter.get_nodes())
bc.write_edges(adapter.get_edges())

# Write admin import statement
bc.write_import_call()

# Print summary
bc.summary()
