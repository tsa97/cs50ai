import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """

    # TODO
    # path = [(109830, 158),(112384, 200)]
    print("source : " + source)
    print("target : " + target)
    path = []
    print("======")
    print("======")
    counterV1 = 1
    cycle = 0
    for neighborV1 in neighbors_for_person(source):
        # Display Seach Result
        print("====len(neighbor) : " + str(neighborV1))
        print("====" + str(movies[neighborV1[0]]["title"]) + " / " + str(people[neighborV1[1]]["name"]))
        print("Explored Actress : " + str(counterV1) + " / " + str(len(neighbors_for_person(source))))
        if neighborV1[1] == target:
            path.append(neighborV1)
            print("FOUND : " + str(target) + " / " + people[target]["name"])
            break
        elif counterV1 == len(neighbors_for_person(source)):
            print("EXPANDING CONNECTION")
            path.append(neighborV1)
            counterV2 = 1
            for neighborV2 in neighbors_for_person(neighborV1[1]):
                # Display Seach Result
                print("EXPANDING CONTACT : " + str(people[neighborV2[1]]["name"]))
                print("====len(neighbor) : " + str(neighborV2))
                print("====" + str(movies[neighborV2[0]]["title"]) + " / " + str(people[neighborV2[1]]["name"]))
                print("Explored Actress : " + str(counterV2) + " / " + str(len(neighbors_for_person(neighborV1[1]))))
                if neighborV2[1] == target:
                    path.append(neighborV2)
                    print("FOUND : " + str(target) + " / " + people[target]["name"])
                    break
                elif counterV2 == len(neighbors_for_person(source)):
                    print("CONNECTION NOT FOUND")
                    # path.append(neighborV2)
                else :
                    counterV2 += 1
        else :
            counterV1 += 1
    cycle += 1

    path = path[-1:]
    print(path)
    # print(path[0][0])
    # print(path[0][1])
    # print(path[1][1])
    # print(path[2])
    # print(people)
    # path.append(158, 109830)
    return path


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
