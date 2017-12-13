import git
import github

from pathlib import Path
from pprint import pprint


def read_oauth_token(oauth_token_file):
	with open(oauth_token_file, 'r') as read_obj:
		for line in read_obj:
			token = line.strip()
			break
	return token


def get_orgs_info(oauth_token):
	my_github = github.Github(login_or_token=oauth_token)
	org_info = {organization.name: organization for organization in my_github.get_user().get_orgs()}
	return org_info


def get_org_repos(org_info):
	org_repos = org_info.get_repos()
	return [repo for repo in org_repos]


def get_repo_urls(repos_info):
	return {repo.name: repo.html_url for repo in repos_info}


def setup_paths(repos_dst=None, token_path=None):
	if not token_path:
		oauth_token_file = Path(__file__).parents[2].joinpath('oauth_token_github_org_names.txt')
	if not repos_dst:
		repos_dst_path = Path(__file__).parents[2].joinpath('all_tic_repos')
	else:
		repos_dst = Path(repos_dst)
		if repos_dst.is_absolute():
			repos_dst_path = repos_dst
		else:
			repos_dst_path = Path(__file__).parents[2].joinpath(repos_dst)
	return oauth_token_file, repos_dst_path


def clone_repos(repo_urls, dst):
	for repo_name, repo_url in repo_urls.items():
		repo_url = '.'.join([repo_url, 'git'])
		repo_dst = dst.joinpath(repo_name)
		try:
			git.Repo.clone_from(url=repo_url, to_path=repo_dst)
		except git.exc.GitCommandError as excep:
			print(excep.stderr)
		else:
			print(f'Cloned {repo_url} to {repo_dst}')

def make_dst_path(dst):
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


def main():
	oauth_token_file, repo_dir_dst = setup_paths()
	make_dst_path(repo_dir_dst)
	token = read_oauth_token(oauth_token_file)
	orgs_info = get_orgs_info(token)
	tic_repos = get_org_repos(orgs_info['The Imaging Collective'])
	repo_urls = get_repo_urls(tic_repos)
	clone_repos(repo_urls=repo_urls, dst=repo_dir_dst)


if __name__ == '__main__':
	main()

