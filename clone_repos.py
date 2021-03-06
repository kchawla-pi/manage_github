# -*- encoding: utf-8 -*-
# !/usr/bin/env python3
"""
Clones all the repos in a GitHub Organization to which the user is a member.
Requires the members user's GitHub token with read:org scope.
Accepts path to token file and destination directory.
"""

import argparse
import git  # pip install gitpython
import github  # pip install PyGithub

from pathlib import Path
from pprint import pprint
from typing import (AnyStr,
                    ByteString,
                    Dict,
                    Iterator,
                    List,
                    Text,
                    Union,
                    NewType,
                    )

GitHubOrganization = NewType('GitHubOrganization', github.Organization)
GitHubRepository = NewType('GitHubRepository', github.Repository)


def read_oauth_token(oauth_token_file: Union[ByteString, AnyStr]) -> Text:
	""" Reads and returns the OAuth Token from the supplied text file.
	"""
	with open(oauth_token_file, 'r') as read_obj:
		token = [line.strip() for line in read_obj if '#' not in line[:2]][0]
	return token


def get_orgs_info(oauth_token: AnyStr) -> Dict[Text, GitHubOrganization]:
	""" Takes a GitHub user's OAuth token and returns dict of their GitHub Organization names and objects.
	"""
	my_github = github.Github(login_or_token=oauth_token)
	org_info = {organization.name: organization for organization in my_github.get_user().get_orgs()}
	return org_info


def _get_org_repos(org_info: Dict[Text, GitHubOrganization]) -> List[GitHubRepository]:
	""" Returns the list of GitHub Repository objects of the user's GitHub organization.
	Accepts a dict of GitHub Organization name and object.
	"""
	org_repos = org_info.get_repos()
	return [repo for repo in org_repos]


def _get_repo_urls(repos_info: Iterator[GitHubRepository]) -> Dict[Text, Text]:
	""" Accepts GitHub Repository objects and returns dict of repository name and HTML url.
	"""
	return {repo.name: repo.html_url for repo in repos_info}


def _clone_repos(repo_urls: Dict[Text, Text], dst: Union[ByteString, AnyStr]):
	""" Git clones repositories whose name and HTML url is supplied as dict to the specified target directory path.
	"""
	for repo_name, repo_url in repo_urls.items():
		repo_url = '.'.join([repo_url, 'git'])
		repo_dst = dst.joinpath(repo_name)
		try:
			git.Repo.clone_from(url=repo_url, to_path=repo_dst)
		except git.exc.GitCommandError as excep:
			print(excep.stderr)
		else:
			print(f'Cloned {repo_url} to {repo_dst}')


def _make_dst_path(dst: Union[ByteString, AnyStr]):
	""" Creates the specified destination directory to clone repositories in.
	Shows error message if a non-empty directory exists, success message on success.
	"""
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


def _get_cli_args() -> argparse.ArgumentParser.parse_args:
	arg_parser = argparse.ArgumentParser(
			description='Clones all the repositories on The Imaging Collective organization on GitHub',
			prog='clone_repos.py',
			usage='py3 %(prog)s destination-containing-directory-path oauth-token-filepath'
			)
	arg_parser.add_argument('dst')
	arg_parser.add_argument('token_file')
	return arg_parser.parse_args()


def clone_org_repos(repo_dir_dst: Union[ByteString, AnyStr], oauth_token_file: Union[ByteString, AnyStr],
                    org_name: Text):
	"""	Clones all the repositories from a Github Organization to a specified local directory.
	Accepts:
     - The destination directory path
     - Path to file with User's OAuth token.
     - Name of the organization.
	"""
	repo_dir_dst = Path(repo_dir_dst)
	oauth_token_file = Path(oauth_token_file)
	_make_dst_path(repo_dir_dst)
	token = read_oauth_token(oauth_token_file)
	orgs_info = get_orgs_info(token)
	tic_repos = _get_org_repos(orgs_info[org_name])
	repo_urls = _get_repo_urls(tic_repos)
	_clone_repos(repo_urls=repo_urls, dst=repo_dir_dst)


def filter_org_repos(repo_list, oauth_token_file: Union[ByteString, AnyStr],
                     org_name: Text):
	oauth_token_file = Path(oauth_token_file)
	token = read_oauth_token(oauth_token_file)
	orgs_info = get_orgs_info(token)
	tic_repos = _get_org_repos(orgs_info[org_name])
	return [repo for repo in tic_repos if repo.full_name.split('/')[-1] in repo_list]
	
	print()

def make_root_path():
	root_file_parts = Path(__file__).parts
	root_part_idx = root_file_parts.index('workspace')
	root_path = Path(*root_file_parts[:root_part_idx + 1])
	return root_path

def clone_cli():
	cli_args = _get_cli_args()
	repo_dir_dst = cli_args.dst
	oauth_token_file = cli_args.token_file
	clone_org_repos(repo_dir_dst, oauth_token_file, org_name='The Imaging Collective')
	

def backup_and_delete():
	root_path = make_root_path()
	repo_delete_token_filepath = root_path.joinpath('oauth_token_github_delete_repos.txt')
	org_read_token_filepath = root_path.joinpath('oauth_token_github_org_names.txt')
	org_repo_clone_path = root_path.joinpath('tic', 'tic_backup_before_delete')
	
	# clone_org_repos(repo_dir_dst=org_repo_clone_path, oauth_token_file=org_read_token_filepath, org_name='The Imaging Collective')
	
	repo_list = Path('~', 'Downloads', 'tic_cleanup.txt').expanduser().read_text().split('\n')
	delete_repos_list = filter_org_repos(repo_list, oauth_token_file=repo_delete_token_filepath, org_name='The Imaging Collective')
	[repo.delete() for repo in delete_repos_list]
	
	
def main():
	backup_and_delete()


if __name__ == '__main__':
	main()
