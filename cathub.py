import json
import requests
import json
import csv

# paperid is the string identifier in catalysis-hub.org
paperid = "CamposEfficient2021"

def main():
    # define query
    params = {
    'query': f'{{reactions(pubId:"{paperid}") {{\n  edges {{\n    node {{\n      Equation\n      chemicalComposition\n      facet\n      reactionEnergy\n      sites\n    }}\n  }}\n}}}}',
    }

    response = requests.get('http://api.catalysis-hub.org/graphql', params=params)

    # convert to json text jfile
    txt = response.text
    jfile = json.loads(txt)


    # extract out the useful data in the json dictionary
    listdata = jfile['data']['reactions']['edges']

    # the column data
    csv_col = ['chemicalComposition', 'Equation', 'sites', 'reactionEnergy' ,'facet']

    # name the csv export file
    csvfile = f"{paperid}.csv"

    # write the data to the csv
    with open(csvfile, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=csv_col)
        writer.writeheader()

        for data in listdata:
            row = data['node']
            writer.writerow(row)





if __name__ == "__main__":
    main()
