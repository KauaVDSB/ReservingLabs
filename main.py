from app import app


if __name__ == "__main__":
    """ Valida e inicia aplicação no servidor. """
    app.run(
        host="0.0.0.0", port=5000, debug=True
    )  # Em modo de desenvolvimento

