#!/usr/bin/env python3
"""Point d'entrée pour l'application d'évaluation TDAH."""

from app import create_app

app = create_app()

if __name__ == '__main__':
    print("=" * 60)
    print("  Application d'Auto-Évaluation TDAH Adulte")
    print("  Ouvrez http://127.0.0.1:5001 dans votre navigateur")
    print("=" * 60)
    app.run(debug=True, host='127.0.0.1', port=5001)
