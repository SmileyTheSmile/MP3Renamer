def capitalize_all_words(string):
    """Capitalizes every word in a string."""
    
    string = string.split()
    
    for i in range(len(string)):
        string[i] = string[i][0].upper() + string[i][1:]
        
    return ' '.join(string)
