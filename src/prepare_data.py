"""Prepara House Prices para análisis exploratorio y modelado de regresión.

El flujo separa la variable objetivo, completa faltantes numéricos de los
predictores y genera dos representaciones de las categorías. SalePrice se
conserva intacta para mantener la trazabilidad de los resultados.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "raw" / "house-prices" / "train.csv"
OUTPUT = ROOT / "data" / "processed"
TARGET = "SalePrice"
IDENTIFIER = "Id"


def main() -> None:
    # Detiene la ejecución si el dataset fuente no se ha incorporado al proyecto.
    if not INPUT.exists():
        raise FileNotFoundError(f"No se encontró el archivo fuente: {INPUT}")

    OUTPUT.mkdir(parents=True, exist_ok=True)

    # Reconoce las dos representaciones habituales de valores faltantes en CSV.
    df = pd.read_csv(INPUT, na_values=["NA"])
    # SalePrice es el resultado a analizar; Id no aporta información predictiva.
    y = df[TARGET].copy()
    X = df.drop(columns=[TARGET, IDENTIFIER]).copy()

    numerical = X.select_dtypes(include="number").columns.tolist()
    categorical = X.select_dtypes(exclude="number").columns.tolist()
    missing_before = X.isna().sum()
    numerical_means = X[numerical].mean()

    # Completa solo predictores numéricos; la variable objetivo no se altera.
    X_imputed = X.copy()
    X_imputed[numerical] = X_imputed[numerical].fillna(numerical_means)

    # Convierte categorías a códigos enteros y conserva una etiqueta para ausencias.
    X_codes = X_imputed.copy()
    category_maps: dict[str, dict[str, int]] = {}
    for column in categorical:
        values = X_codes[column].fillna("Sin_dato").astype(str)
        codes, labels = pd.factorize(values, sort=True)
        X_codes[column] = codes
        category_maps[column] = {label: int(index) for index, label in enumerate(labels)}

    # Crea indicadores 0/1 para análisis que no requiere orden entre categorías.
    X_dummies = pd.get_dummies(
        X_imputed.assign(**{c: X_imputed[c].fillna("Sin_dato") for c in categorical}),
        columns=categorical,
        dtype=int,
    )

    profile = {
        "observations": int(df.shape[0]),
        "variables_total": int(df.shape[1]),
        "target": TARGET,
        "identifier_excluded": IDENTIFIER,
        "predictors": int(X.shape[1]),
        "numeric_predictors": numerical,
        "categorical_predictors": categorical,
        "missing_numeric_before_imputation": {
            column: int(missing_before[column])
            for column in numerical
            if missing_before[column] > 0
        },
        "missing_categorical": {
            column: int(missing_before[column])
            for column in categorical
            if missing_before[column] > 0
        },
        "dummy_features": int(X_dummies.shape[1]),
    }

    # Guarda cada resultado por separado para que el flujo sea auditable.
    X_imputed.to_csv(OUTPUT / "X_numeric_imputed.csv", index=False)
    X_codes.to_csv(OUTPUT / "X_categorical_codes.csv", index=False)
    X_dummies.to_csv(OUTPUT / "X_dummies.csv", index=False)
    y.to_frame(name=TARGET).to_csv(OUTPUT / "y_sale_price.csv", index=False)
    pd.DataFrame({"variable": numerical, "mean": numerical_means.values}).to_csv(
        OUTPUT / "numeric_means_used.csv", index=False
    )
    (OUTPUT / "category_code_maps.json").write_text(
        json.dumps(category_maps, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (OUTPUT / "dataset_profile.json").write_text(
        json.dumps(profile, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print("Preparación completada")
    print(json.dumps(profile, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
