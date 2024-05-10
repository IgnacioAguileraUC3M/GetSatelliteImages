
import strategies

def select_image(images: list[dict], selection_strategy: str) -> dict:
    '''
    Image selection strategies:
        - latest
        - has specified coordinate most centered
        - Lowest cloud coverage
        - Clesest to specified date
        - Contiains specified attribute
        - Contains specified polygon
    '''

    selected_image = strategies.get_selection_strategy(selection_strategy)(images)
    return selected_image