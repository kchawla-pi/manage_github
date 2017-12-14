# encoding: -*-utf-8 -*-
#!/usr/bin/env python3
"""
Clones all the repos in a GitHub Organization to which the user is a member.
Requires the members user's GitHub token with read:org scope.
Accepts path to token file and destination directory.
"""

import argparse
import git
import github

from pathlib import Path
from pprint import pprint
from typing import (AnyStr, ByteString, Dict, List, Text, Union,)


def read_oauth_token(oauth_token_file: Union[ByteString, AnyStr]) -> Text:
	with open(oauth_token_file, 'r') as read_obj:
		token = [line.strip() for line in read_obj if '#' not in line[:2]][0]
	return token


def get_orgs_info(oauth_token: AnyStr) -> Dict[Text, github.Organization]:
	my_github = github.Github(login_or_token=oauth_token)
	org_info = {organization.name: organization for organization in my_github.get_user().get_orgs()}
	return org_info


def get_org_repos(org_info: Dict[Text, github.Organization]) -> List[github.Repository]:
	org_repos = org_info.get_repos()
	return [repo for repo in org_repos]


def get_repo_urls(repos_info: github.Repository) -> Dict[Text, Text]:
	return {repo.name: repo.html_url for repo in repos_info}


def clone_repos(repo_urls: Dict[Text, Text], dst: Union[ByteString, AnyStr]):
	for repo_name, repo_url in repo_urls.items():
		repo_url = '.'.join([repo_url, 'git'])
		repo_dst = dst.joinpath(repo_name)
		try:
			git.Repo.clone_from(url=repo_url, to_path=repo_dst)
		except git.exc.GitCommandError as excep:
			print(excep.stderr)
		else:
			print(f'Cloned {repo_url} to {repo_dst}')


def make_dst_path(dst: Union[ByteString, AnyStr]):
	try:
		dst.mkdir()
	except FileExistsError as excep:
		print(f'A non-empty directory `{dst.name}` already exists at `{dst.parent}.\n'
		      f'An empty directory is necessary for this operation.\n'
		      f'Delete existing destination directory or choose a different name or location.\n'
		      f'Then try again.\n'
		      f'STOPPING. ({str(excep)}).\n'
		      )
		quit()
	else:
		print(f'`{dst.name}` created at `{dst.parent}`')

def get_cli_args() -> argparse.ArgumentParser.parse_args:
	arg_parser = argparse.ArgumentParser(description='Clones all the repositories on The Imaging Collective organization on GitHub',
	                                     prog='clone_repos.py',
	                                     usage='py3 %(prog)s destination-containing-directory-path oauth-token-filepath'
	                                     )
	arg_parser.add_argument('dst')
	arg_parser.add_argument('token_file')
	return arg_parser.parse_args()

def clone_tic(repo_dir_dst: Union[ByteString, AnyStr], oauth_token_file: Union[ByteString, AnyStr]):
	repo_dir_dst = Path(repo_dir_dst)
	oauth_token_file = Path(oauth_token_file)
	make_dst_path(repo_dir_dst)
	token = read_oauth_token(oauth_token_file)
	orgs_info = get_orgs_info(token)
	tic_repos = get_org_repos(orgs_info['The Imaging Collective'])
	repo_urls = get_repo_urls(tic_repos)
	clone_repos(repo_urls=repo_urls, dst=repo_dir_dst)


def main():
	cli_args = get_cli_args()
	repo_dir_dst = cli_args.dst
	oauth_token_file = cli_args.token_file
	clone_tic(repo_dir_dst, oauth_token_file)



if __name__ == '__main__':
	main()

