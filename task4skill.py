import pandas as pd
import matplotlib.pyplot as plt
import os

# ---------------- CONFIG ----------------
file_path = r"C:\Users\laasy\OneDrive\Desktop\SCT_DS_4\RTA Dataset.csv"
output_path = r"C:\Users\laasy\OneDrive\Desktop\SCT_DS_4\output"
os.makedirs(output_path, exist_ok=True)

# ---------------- LOAD DATA ----------------
if not os.path.exists(file_path):
    raise FileNotFoundError(f"Dataset not found at {file_path}")

df = pd.read_csv(file_path)
df.dropna(how="all", inplace=True)

# Convert Time to Hour if present
if "Time" in df.columns:
    try:
        df["Time"] = pd.to_datetime(df["Time"], errors="coerce")
        df["Hour"] = df["Time"].dt.hour
    except:
        pass

# --- Pick usable columns ---
usable_cols = [c for c in df.columns if df[c].notna().sum() > 0]

# --- Prefer categorical columns first ---
categorical_cols = [c for c in usable_cols if df[c].dtype == "object" and df[c].nunique() <= 20]
numeric_cols = [c for c in usable_cols if df[c].dtype != "object"]

# Take first 8 best columns for visualization
selected_cols = (categorical_cols[:6] + numeric_cols[:6])[:8]

if len(selected_cols) < 8:
    print(f"⚠️ Only {len(selected_cols)} usable columns found, showing what exists.")

grid1_cols = selected_cols[:4]
grid2_cols = selected_cols[4:8]

# --- Function to create Grid 1 ---
def make_grid1(cols):
    fig, axs = plt.subplots(2, 2, figsize=(11, 7))
    fig.suptitle("Grid 1", fontsize=13, fontweight="bold")
    axs = axs.flatten()

    for ax, col in zip(axs, cols):
        vc = df[col].dropna()
        if vc.dtype == "object" or vc.nunique() < 15:
            vc.value_counts().plot(kind="bar", ax=ax, color="skyblue")
        else:
            vc.value_counts().sort_index().plot(kind="bar", ax=ax, color="skyblue")

        ax.set_title(col, fontsize=11)
        ax.tick_params(axis="x", rotation=30)

    plt.tight_layout(rect=[0, 0, 1, 0.93])
    save_path = os.path.join(output_path, "grid1.png")
    fig.savefig(save_path)
    print(f"✅ Grid 1 saved at {save_path}")
    plt.show()

# --- Function to create Grid 2 ---
def make_grid2(cols):
    fig, axs = plt.subplots(2, 2, figsize=(11, 7))
    fig.suptitle("Grid 2", fontsize=13, fontweight="bold")
    axs = axs.flatten()

    for ax, col in zip(axs, cols):
        vc = df[col].dropna()

        # --- Special handling for Time/Hour ---
        if col in ["Time", "Hour"]:
            if "Hour" in df.columns and df["Hour"].notna().sum() > 0:
                hour_counts = df["Hour"].value_counts().sort_index()
                hour_counts.plot(kind="line", marker="o", ax=ax, color="purple")
                ax.set_title("Accidents by Hour", fontsize=11)
                ax.set_xlabel("Hour of Day")
                ax.set_ylabel("Count")
            else:
                ax.text(0.5, 0.5, "No Time Data", ha="center", va="center")
                ax.set_axis_off()

        # --- Categorical or small-numeric columns ---
        elif vc.dtype == "object" or vc.nunique() < 15:
            vc.value_counts().plot(kind="bar", ax=ax, color="orange")

        # --- Continuous numeric columns ---
        else:
            vc.plot(kind="hist", bins=15, ax=ax, color="green")

        ax.set_title(col, fontsize=11)
        ax.tick_params(axis="x", rotation=30)

    plt.tight_layout(rect=[0, 0, 1, 0.93])
    save_path = os.path.join(output_path, "grid2.png")
    fig.savefig(save_path)
    print(f"✅ Grid 2 saved at {save_path}")
    plt.show()

# --- Display both grids ---
if grid1_cols:
    make_grid1(grid1_cols)

if grid2_cols:
    make_grid2(grid2_cols)

print("✅ Both grids displayed successfully.")
