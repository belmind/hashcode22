from collections import defaultdict


# Solver that takes an input as a file object,
# and returns the output as a string
def solve(input):
    first_line = input.readline().strip().split(' ')
    nr_contributors = int(first_line[0])
    nr_projects = int(first_line[1])

    contributors = defaultdict(list)
    projects = []
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
        project = {
            'name': name,
            'completion': completion,
            'score': score,
            'best_before': best_before,
            'nr_roles': int(nr_roles),
        }
        req_skills = []

        for _ in range(int(nr_roles)):
            skill_name, skill_level = input.readline().strip().split(' ')
            req_skills.append((skill_name, int(skill_level)))

        project['req_skills'] = req_skills
        projects.append(project)

    # Solution

    finalProjects = []

    sorted_projects = sorted(projects, key=lambda x: x['best_before'])
    for project in sorted_projects:
        chosenContributors = []
        chosenContributorSet = set()
        for (skill_name, required_skill_level) in project['req_skills']:
            try:
                (contributor, contributor_skill_level) = min([x for x in roles[skill_name] if x[1] >= required_skill_level and x[0] not in chosenContributorSet], key=lambda x: x[1])
                chosenContributors.append(contributor)
                chosenContributorSet.add(contributor)

            except ValueError:
                # Mentoring logic
                for chosenContributor in chosenContributors:
                    for (contributor_skill_name, contributor_skill_level) in contributors[chosenContributor]:
                        if contributor_skill_name == skill_name and contributor_skill_level >= required_skill_level:
                            potentialContributors = [x for x in roles[skill_name] if x[1] == required_skill_level - 1 and x[0] not in chosenContributorSet]
                            if potentialContributors:
                                (contributor, contributor_skill_level) = min(potentialContributors, key=lambda x: x[1])
                                chosenContributors.append(contributor)
                                chosenContributorSet.add(contributor)
                break

        if (len(chosenContributors) == project['nr_roles']):
            finalProjects.append((project['name'], chosenContributors))

    output = f"""{len(finalProjects)}"""

    for (project, chosenContributors) in finalProjects:
        output += f"""\n{project}\n{" ".join(chosenContributors)}"""

    return output
