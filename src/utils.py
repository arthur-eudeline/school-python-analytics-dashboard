def convertDate(date, df, minDate: bool):
    if date is None:
        if minDate:
            date = df.index.min()
        else:
            date = df.index.max()

    # Reformate les date de fin pour les utiliser dans df.loc
    date = str(date).split(" ")[0]
    date = str(date).split("T")[0]

    return date
