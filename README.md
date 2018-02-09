# manage_git README
Originally, this was a repo with programs written to manage the TIC organization on GitHub (https://github.com/theimagingcollective/).  
Now it will be adopted to manage any github user/organization in general.

clone_repos.py requires a GitHUb OAuth Token for the user who wishes to clone the repos of any organzation they are a member of.
The token can be obtained from User's Settings on Github.com

Steps to obtain the token:

1. Login to you Github account.  
2. Click on your User logo in the top right corner.  
3. In the drop-down menu, click `Settings`.  
4. In the left-hand side pane, click on `Personal Access Tokens` or `Developer Options` and then `Personal Access Tokens`.
5. Click on `Generate New Token`.  
6. Give a clear description of the purpose of the new token. `Reading user's organization information for pygithub`.  
7. In `Select scopes`, go to the section for `admin: org`.  
8. Check mark enable the `read: org` permission, leave the rest unchecked.  
9. Click on `Generate Token`.
10. Copy and paste the new token into a text file. Save it at a convenient location for you intended backup directory. Lines preceded with a `#` are considered to be comments.
11. Do not share the token casually.

To run type:

	$ python3 <path to clone_repos.py>/clone_repos.py <path to destination directory> <path to oauth token file> 





