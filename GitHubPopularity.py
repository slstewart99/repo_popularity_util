#!/usr/bin/env python3
# -*- coding: cp1252 -*-
""" cp1252 = Windows encoding """

import sys
import setuptools
import textwrap
import json 
import requests

# NOTE: This program requires third party library PyGithub to be installed,
#   it can be found at:
#   Code Repo:   https://github.com/PyGithub/PyGithub
#   Information: https://pygithub.readthedocs.io/en/latest/
#   (Github only offers official client libraries for Ruby, Node.js and .NET)

def usage_help():
    print ("\n Option I of II:  GitHubPopularity command, Public Organization Repo Inquiry:")
    print (" $ GitHubPopularity.py <GITHub_organization> <number_of_statistics_desired>")
    print (" Example command:")
    print (" $ GitHubPopularity Atlassian 3\n")
    print ("\n Option II of II: GitHubPopularity command, Private User Repo Inquiry:")
    print (" $ GitHubPopularity.py <username> <number_of_statistics_desired> <40_alpanumeric_token>")
    print (" Example command:")
    print (" $ GitHubPopularity joeblow 3 65fc6d4046eb53781288b93a7868f743cd00dc8e\n")

def main():
    if (len(sys.argv) != 3) and (len(sys.argv) != 4):
        usage_help()
        sys.exit(1)

    if len(sys.argv) == 3:
        orgName = sys.argv[1]
        nNum    = sys.argv[2]
        repos_url = 'https://api.github.com/orgs/' + orgName + '/repos'
        print("\nrepo_url: ", repos_url)
    else:
        username = sys.argv[1] 
        nNum     = sys.argv[2] 
        token    = sys.argv[3] 
        repos_url = 'https://api.github.com/user/repos'
        print('\nExamining repos of GITHub user:', username) 

    # create a re-usable session object
    gh_session = requests.Session()
    if len(sys.argv) == 4:
        gh_session.auth = (username, token)

    # get the list of repos belonging to 'repos_url'
    repos = json.loads(gh_session.get(repos_url).text)
    #print(repos) # To print contents of each repo - can be very lengthy!

    print("---------------------------------------------------")
    print("A list of all repo names:")
    print("  ----------")
    for repo in repos:
        print (repo["name"])
    print ("---------------------------------------------------")

    # Create empty dictionaries
    starsDict = {}
    forksDict = {}
    pullsDict = {}
    contsDict = {}

    for repo in repos:
        # Insert each parameter value into its proper dictionary 
        starsDict[repo['name']] = repo['stargazers_count']
        forksDict[repo['name']] = repo['forks_count']

        if len(sys.argv) == 3:
            pull_url = 'https://api.github.com/orgs/' + orgName + '/' + repo['name'] + '/pulls'
        else:
            pull_url = 'https://api.github.com/user/' + repo['name'] + '/pulls'
            
        pulls = json.loads(gh_session.get(pull_url).text)
        i = 0
        for pull in pulls:
            i += 1
        pullsDict[repo['name']] = i

        if repo['forks_count'] >= 1:
            contsDict[repo['name']] = i / repo['forks_count']
        else:
            contsDict[repo['name']] = 0

    print("The desired top number of sorted results from CLI input: ", nNum)

    listofTuples1 = sorted(starsDict.items(), reverse=True, key=lambda x: x[1])
    # Iterate over the sorted sequence
    for elem in listofTuples1[0:int(nNum)]:
        print("Stars: ", elem[0] , " ::" , elem[1] )

    listofTuples2 = sorted(forksDict.items(), reverse=True, key=lambda x: x[1])
    # Iterate over the sorted sequence
    for elem in listofTuples2[0:int(nNum)]:
        print("Forks: ", elem[0] , " ::" , elem[1] )

    listofTuples3 = sorted(pullsDict.items(), reverse=True, key=lambda x: x[1])
    # Iterate over the sorted sequence
    for elem in listofTuples3[0:int(nNum)]:
        print("Pulls: ",elem[0] , " ::" , elem[1] )

    listofTuples4 = sorted(contsDict.items(), reverse=True, key=lambda x: x[1])
    # Iterate over the sorted sequence
    for elem in listofTuples4[0:int(nNum)]:
        print("Contribution %: ", elem[0] , " ::" , elem[1] )        

# Standard boilerplate to call main()
if __name__ == '__main__':
  main()
  
