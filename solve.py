from collections import defaultdict
from multiprocessing.sharedctypes import Value


# Solver that takes an input as a file object,
# and returns the output as a string
def solve(input):
    first_line = input.readline().strip().split(' ')
    nr_contributors = int(first_line[0])
    nr_projects = int(first_line[1])

    contributors = defaultdict(list)
    projects = defaultdict(dict)
    roles = defaultdict(list)

    # parsing contributors and skills
    for _ in range(nr_contributors):
        name, nr_skills = input.readline().strip().split(' ')

        # for each contributor
        for _ in range(int(nr_skills)):
            skill_name, skill_level = input.readline().strip().split(' ')
            contributors[name].append((skill_name, int(skill_level)))
            roles[skill_name].append((name, int(skill_level))) # IMPROVE: SORT?

    # for each project
    for _ in range(nr_projects):
        temp = input.readline().strip().split(' ')
        name, completion, score, best_before, nr_roles = temp
        projects[name] = {
            'completion': completion,
            'score': score,
            'best_before': best_before,
            'nr_roles': int(nr_roles),
        }
        req_skills = []

        for _ in range(int(nr_roles)):
            skill_name, skill_level = input.readline().strip().split(' ')
            req_skills.append((skill_name, int(skill_level)))

        projects[name]['req_skills'] = req_skills

    # Solution

    finalProjects = []
    skippedProjects = defaultdict(dict)
    leveledUp = set()
    for (name, data) in projects.items():
        chosenContributors = []
        chosenContributorSet = set()
        toLevelUp = set()
        for (skill_name, req_skill_level) in data['req_skills']:
            try:
                (contributor, contributor_skill_level) = min([x for x in roles[skill_name] if x[1] >= req_skill_level and x[0] not in chosenContributorSet], key=lambda x: x[1])
                chosenContributors.append(contributor)
                chosenContributorSet.add(contributor)
                if contributor_skill_level == req_skill_level and contributor not in leveledUp:
                    toLevelUp.add((contributor, skill_name, contributor_skill_level))
            except ValueError:
                skippedProjects[name] = data
                break
        if (len(chosenContributors) == data['nr_roles']):
            finalProjects.append((name, chosenContributors))
            for (contributor, skill_name, contributor_skill_level) in toLevelUp:
                if contributor in toLevelUp:
                    roles[skill_name].remove((contributor, contributor_skill_level))
                    roles[skill_name].append((contributor, contributor_skill_level + 1))
                    leveledUp.add(contributor)

    for (name, data) in skippedProjects.items():
        chosenContributors = []
        chosenContributorSet = set()
        for (skill_name, req_skill_level) in data['req_skills']:
            try:
                (contributor, contributor_skill_level) = min([x for x in roles[skill_name] if x[1] >= req_skill_level and x[0] not in chosenContributorSet], key=lambda x: x[1])
                chosenContributors.append(contributor)
                chosenContributorSet.add(contributor)
            except ValueError:
                break
        if (len(chosenContributors) == data['nr_roles']):
            finalProjects.append((name, chosenContributors))

    output = f"""{len(finalProjects)}"""

    for (project, chosenContributors) in finalProjects:
        output += f"""\n{project}\n{" ".join(chosenContributors)}"""

    return output