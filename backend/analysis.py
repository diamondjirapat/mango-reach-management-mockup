def calculate_score(click_count: int, cost: float, source: str) -> float:
    """
    Calculate a score for the ad based on click count, cost, and source.
    Score = (Clicks / Cost) * SourceWeight
    """
    if cost == 0:
        return 0.0
    
    source_weights = {
        "Facebook": 1.2,
        "X": 1.1,
        "Instagram": 1.3,
        "Google": 1.4,
        "TikTok": 1.5,
        "Flyers": 0.5,
        "Billboard": 0.8,
        "Unknown": 0.1
    }
    
    weight = source_weights.get(source, 1.0)

    raw_efficiency = click_count / cost
    score = raw_efficiency * weight * 10 # Scale up
    
    return round(score, 2)
