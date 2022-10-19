# This file generates the html blocks for displaying multiple movies in a row by row manner.

def generate_html_block(movie):
    """
    Generates the boilerplate movie block HTML to be embedded.
    takes a dictionary of the form

    movie = {"year": film.year, "title": film.title, "poster": film.poster, "overview": film.overview}

    * Doesn't actually have to be a film, but that's the primary purpose.
    """
    movie_format = f"""
    <div class='movie'>
            
            <div class='poster-details-parent'>

                <div class='poster'><img src ='{movie["poster"]}'></div>

                <div class='details'>

                    <h1>{movie["title"]} {movie["year"]}</h1>

                {movie["overview"]}
                </div>

            </div>

        </div>"""
    return movie_format
