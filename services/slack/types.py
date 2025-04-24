from rid_lib.core import ORN

class GithubCommit(ORN):
    """
    Resource Identifier (RID) for a specific GitHub commit.
    
    Format: orn:github.commit:<owner>/<repo>/<sha>
    Example: orn:github.commit:microsoft/vscode/a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0
    """
    namespace = "github.commit"

    def __init__(self, owner: str, repo: str, sha: str):
        """
        Initialize a GitHub commit RID.
        
        Args:
            owner: The repository owner (user or organization)
            repo: The repository name
            sha: The commit SHA (full 40-character or shortened)
        """
        if not owner or not repo or not sha:
            raise ValueError("Owner, repo, and SHA cannot be empty")
        
        if "/" in owner or "/" in repo:
            raise ValueError("Owner and repo cannot contain '/' character")
            
        self.owner = owner
        self.repo = repo
        self.sha = sha

    @property
    def reference(self) -> str:
        """Returns the reference part of the RID: '<owner>/<repo>/<sha>'."""
        return f"{self.owner}/{self.repo}/{self.sha}"
    
    @property
    def repository_full_name(self) -> str:
        """Returns the full repository name: '<owner>/<repo>'."""
        return f"{self.owner}/{self.repo}"
    
    @property
    def html_url(self) -> str:
        """Returns the HTML URL to view this commit on GitHub."""
        return f"https://github.com/{self.owner}/{self.repo}/commit/{self.sha}"
    
    @property
    def api_url(self) -> str:
        """Returns the GitHub API URL for this commit."""
        return f"https://api.github.com/repos/{self.owner}/{self.repo}/commits/{self.sha}"

    @classmethod
    def from_reference(cls, reference: str) -> "GithubCommit":
        """
        Creates a GithubCommit instance from its reference string.
        
        Args:
            reference: String in format '<owner>/<repo>/<sha>'
            
        Returns:
            GithubCommit instance
            
        Raises:
            ValueError: If the reference format is invalid
        """
        try:
            parts = reference.split("/", maxsplit=2)
            if len(parts) != 3:
                raise ValueError("Reference must contain exactly two '/' separators")
                
            owner, repo, sha = parts
            
            if not owner or not repo or not sha:
                raise ValueError("Owner, repo, and SHA parts cannot be empty")
                
            # Basic SHA length check
            if len(sha) < 7:  # Minimum length for a short SHA
                raise ValueError(f"SHA part seems too short: {sha}")
                
            return cls(owner=owner, repo=repo, sha=sha)
            
        except ValueError as e:
            raise ValueError(f"Invalid reference format for GithubCommit. Expected '<owner>/<repo>/<sha>', got '{reference}'. Error: {e}") from e
        except Exception as e:
            raise TypeError(f"Unexpected error parsing GithubCommit reference '{reference}': {e}") from e


class GithubIssue(ORN):
    """
    Resource Identifier (RID) for a specific GitHub issue.
    
    Format: orn:github.issue:<owner>/<repo>/<number>
    Example: orn:github.issue:microsoft/vscode/12345
    """
    namespace = "github.issue"

    def __init__(self, owner: str, repo: str, number: str):
        """
        Initialize a GitHub issue RID.
        
        Args:
            owner: The repository owner (user or organization)
            repo: The repository name
            number: The issue number (as a string)
        """
        if not owner or not repo or not number:
            raise ValueError("Owner, repo, and issue number cannot be empty")
            
        if "/" in owner or "/" in repo:
            raise ValueError("Owner and repo cannot contain '/' character")
            
        # Validate issue number is numeric
        try:
            int(number)
        except ValueError:
            raise ValueError(f"Issue number must be numeric: {number}")
            
        self.owner = owner
        self.repo = repo
        self.number = number

    @property
    def reference(self) -> str:
        """Returns the reference part of the RID: '<owner>/<repo>/<number>'."""
        return f"{self.owner}/{self.repo}/{self.number}"
    
    @property
    def repository_full_name(self) -> str:
        """Returns the full repository name: '<owner>/<repo>'."""
        return f"{self.owner}/{self.repo}"
    
    @property
    def html_url(self) -> str:
        """Returns the HTML URL to view this issue on GitHub."""
        return f"https://github.com/{self.owner}/{self.repo}/issues/{self.number}"
    
    @property
    def api_url(self) -> str:
        """Returns the GitHub API URL for this issue."""
        return f"https://api.github.com/repos/{self.owner}/{self.repo}/issues/{self.number}"

    @classmethod
    def from_reference(cls, reference: str) -> "GithubIssue":
        """
        Creates a GithubIssue instance from its reference string.
        
        Args:
            reference: String in format '<owner>/<repo>/<number>'
            
        Returns:
            GithubIssue instance
            
        Raises:
            ValueError: If the reference format is invalid
        """
        try:
            parts = reference.split("/", maxsplit=2)
            if len(parts) != 3:
                raise ValueError("Reference must contain exactly two '/' separators")
                
            owner, repo, number = parts
            
            if not owner or not repo or not number:
                raise ValueError("Owner, repo, and issue number parts cannot be empty")
                
            # Validate issue number is numeric
            try:
                int(number)
            except ValueError:
                raise ValueError(f"Issue number must be numeric: {number}")
                
            return cls(owner=owner, repo=repo, number=number)
            
        except ValueError as e:
            raise ValueError(f"Invalid reference format for GithubIssue. Expected '<owner>/<repo>/<number>', got '{reference}'. Error: {e}") from e
        except Exception as e:
            raise TypeError(f"Unexpected error parsing GithubIssue reference '{reference}': {e}") from e


class GithubPullRequest(ORN):
    """
    Resource Identifier (RID) for a specific GitHub pull request.
    
    Format: orn:github.pull:<owner>/<repo>/<number>
    Example: orn:github.pull:microsoft/vscode/6789
    """
    namespace = "github.pull"

    def __init__(self, owner: str, repo: str, number: str):
        """
        Initialize a GitHub pull request RID.
        
        Args:
            owner: The repository owner (user or organization)
            repo: The repository name
            number: The pull request number (as a string)
        """
        if not owner or not repo or not number:
            raise ValueError("Owner, repo, and PR number cannot be empty")
            
        if "/" in owner or "/" in repo:
            raise ValueError("Owner and repo cannot contain '/' character")
            
        # Validate PR number is numeric
        try:
            int(number)
        except ValueError:
            raise ValueError(f"Pull request number must be numeric: {number}")
            
        self.owner = owner
        self.repo = repo
        self.number = number

    @property
    def reference(self) -> str:
        """Returns the reference part of the RID: '<owner>/<repo>/<number>'."""
        return f"{self.owner}/{self.repo}/{self.number}"
    
    @property
    def repository_full_name(self) -> str:
        """Returns the full repository name: '<owner>/<repo>'."""
        return f"{self.owner}/{self.repo}"
    
    @property
    def html_url(self) -> str:
        """Returns the HTML URL to view this pull request on GitHub."""
        return f"https://github.com/{self.owner}/{self.repo}/pull/{self.number}"
    
    @property
    def api_url(self) -> str:
        """Returns the GitHub API URL for this pull request."""
        return f"https://api.github.com/repos/{self.owner}/{self.repo}/pulls/{self.number}"

    @classmethod
    def from_reference(cls, reference: str) -> "GithubPullRequest":
        """
        Creates a GithubPullRequest instance from its reference string.
        
        Args:
            reference: String in format '<owner>/<repo>/<number>'
            
        Returns:
            GithubPullRequest instance
            
        Raises:
            ValueError: If the reference format is invalid
        """
        try:
            parts = reference.split("/", maxsplit=2)
            if len(parts) != 3:
                raise ValueError("Reference must contain exactly two '/' separators")
                
            owner, repo, number = parts
            
            if not owner or not repo or not number:
                raise ValueError("Owner, repo, and PR number parts cannot be empty")
                
            # Validate PR number is numeric
            try:
                int(number)
            except ValueError:
                raise ValueError(f"Pull request number must be numeric: {number}")
                
            return cls(owner=owner, repo=repo, number=number)
            
        except ValueError as e:
            raise ValueError(f"Invalid reference format for GithubPullRequest. Expected '<owner>/<repo>/<number>', got '{reference}'. Error: {e}") from e
        except Exception as e:
            raise TypeError(f"Unexpected error parsing GithubPullRequest reference '{reference}': {e}") from e


class GithubRelease(ORN):
    """
    Resource Identifier (RID) for a specific GitHub release.
    
    Format: orn:github.release:<owner>/<repo>/<tag>
    Example: orn:github.release:microsoft/vscode/v1.60.0
    """
    namespace = "github.release"

    def __init__(self, owner: str, repo: str, tag: str):
        """
        Initialize a GitHub release RID.
        
        Args:
            owner: The repository owner (user or organization)
            repo: The repository name
            tag: The release tag
        """
        if not owner or not repo or not tag:
            raise ValueError("Owner, repo, and tag cannot be empty")
            
        if "/" in owner or "/" in repo or "/" in tag:
            raise ValueError("Owner, repo, and tag cannot contain '/' character")
            
        self.owner = owner
        self.repo = repo
        self.tag = tag

    @property
    def reference(self) -> str:
        """Returns the reference part of the RID: '<owner>/<repo>/<tag>'."""
        return f"{self.owner}/{self.repo}/{self.tag}"
    
    @property
    def repository_full_name(self) -> str:
        """Returns the full repository name: '<owner>/<repo>'."""
        return f"{self.owner}/{self.repo}"
    
    @property
    def html_url(self) -> str:
        """Returns the HTML URL to view this release on GitHub."""
        return f"https://github.com/{self.owner}/{self.repo}/releases/tag/{self.tag}"
    
    @property
    def api_url(self) -> str:
        """Returns the GitHub API URL for this release."""
        return f"https://api.github.com/repos/{self.owner}/{self.repo}/releases/tags/{self.tag}"

    @classmethod
    def from_reference(cls, reference: str) -> "GithubRelease":
        """
        Creates a GithubRelease instance from its reference string.
        
        Args:
            reference: String in format '<owner>/<repo>/<tag>'
            
        Returns:
            GithubRelease instance
            
        Raises:
            ValueError: If the reference format is invalid
        """
        try:
            parts = reference.split("/", maxsplit=2)
            if len(parts) != 3:
                raise ValueError("Reference must contain exactly two '/' separators")
                
            owner, repo, tag = parts
            
            if not owner or not repo or not tag:
                raise ValueError("Owner, repo, and tag parts cannot be empty")
                
            return cls(owner=owner, repo=repo, tag=tag)
            
        except ValueError as e:
            raise ValueError(f"Invalid reference format for GithubRelease. Expected '<owner>/<repo>/<tag>', got '{reference}'. Error: {e}") from e
        except Exception as e:
            raise TypeError(f"Unexpected error parsing GithubRelease reference '{reference}': {e}") from e


class GithubRepository(ORN):
    """
    Resource Identifier (RID) for a GitHub repository.
    
    Format: orn:github.repo:<owner>/<repo>
    Example: orn:github.repo:microsoft/vscode
    """
    namespace = "github.repo"

    def __init__(self, owner: str, repo: str):
        """
        Initialize a GitHub repository RID.
        
        Args:
            owner: The repository owner (user or organization)
            repo: The repository name
        """
        if not owner or not repo:
            raise ValueError("Owner and repo cannot be empty")
            
        if "/" in owner or "/" in repo:
            raise ValueError("Owner and repo cannot contain '/' character")
            
        self.owner = owner
        self.repo = repo

    @property
    def reference(self) -> str:
        """Returns the reference part of the RID: '<owner>/<repo>'."""
        return f"{self.owner}/{self.repo}"
    
    @property
    def repository_full_name(self) -> str:
        """Returns the full repository name: '<owner>/<repo>'."""
        return f"{self.owner}/{self.repo}"
    
    @property
    def html_url(self) -> str:
        """Returns the HTML URL to view this repository on GitHub."""
        return f"https://github.com/{self.owner}/{self.repo}"
    
    @property
    def api_url(self) -> str:
        """Returns the GitHub API URL for this repository."""
        return f"https://api.github.com/repos/{self.owner}/{self.repo}"

    @classmethod
    def from_reference(cls, reference: str) -> "GithubRepository":
        """
        Creates a GithubRepository instance from its reference string.
        
        Args:
            reference: String in format '<owner>/<repo>'
            
        Returns:
            GithubRepository instance
            
        Raises:
            ValueError: If the reference format is invalid
        """
        try:
            parts = reference.split("/")
            if len(parts) != 2:
                raise ValueError("Reference must contain exactly one '/' separator")
                
            owner, repo = parts
            
            if not owner or not repo:
                raise ValueError("Owner and repo parts cannot be empty")
                
            return cls(owner=owner, repo=repo)
            
        except ValueError as e:
            raise ValueError(f"Invalid reference format for GithubRepository. Expected '<owner>/<repo>', got '{reference}'. Error: {e}") from e
        except Exception as e:
            raise TypeError(f"Unexpected error parsing GithubRepository reference '{reference}': {e}") from e


class GithubUser(ORN):
    """
    Resource Identifier (RID) for a GitHub user or organization.
    
    Format: orn:github.user:<username>
    Example: orn:github.user:octocat
    """
    namespace = "github.user"

    def __init__(self, username: str):
        """
        Initialize a GitHub user RID.
        
        Args:
            username: The GitHub username
        """
        if not username:
            raise ValueError("Username cannot be empty")
            
        if "/" in username:
            raise ValueError("Username cannot contain '/' character")
            
        self.username = username

    @property
    def reference(self) -> str:
        """Returns the reference part of the RID: '<username>'."""
        return self.username
    
    @property
    def html_url(self) -> str:
        """Returns the HTML URL to view this user on GitHub."""
        return f"https://github.com/{self.username}"
    
    @property
    def api_url(self) -> str:
        """Returns the GitHub API URL for this user."""
        return f"https://api.github.com/users/{self.username}"

    @classmethod
    def from_reference(cls, reference: str) -> "GithubUser":
        """
        Creates a GithubUser instance from its reference string.
        
        Args:
            reference: String containing the username
            
        Returns:
            GithubUser instance
            
        Raises:
            ValueError: If the reference format is invalid
        """
        try:
            if not reference:
                raise ValueError("Username cannot be empty")
                
            if "/" in reference:
                raise ValueError("Username cannot contain '/' character")
                
            return cls(username=reference)
            
        except ValueError as e:
            raise ValueError(f"Invalid reference format for GithubUser. Expected '<username>', got '{reference}'. Error: {e}") from e
        except Exception as e:
            raise TypeError(f"Unexpected error parsing GithubUser reference '{reference}': {e}") from e


class GithubDiscussion(ORN):
    """
    Resource Identifier (RID) for a GitHub discussion.
    
    Format: orn:github.discussion:<owner>/<repo>/<number>
    Example: orn:github.discussion:microsoft/vscode/4242
    """
    namespace = "github.discussion"

    def __init__(self, owner: str, repo: str, number: str):
        """
        Initialize a GitHub discussion RID.
        
        Args:
            owner: The repository owner (user or organization)
            repo: The repository name
            number: The discussion number (as a string)
        """
        if not owner or not repo or not number:
            raise ValueError("Owner, repo, and discussion number cannot be empty")
            
        if "/" in owner or "/" in repo:
            raise ValueError("Owner and repo cannot contain '/' character")
            
        # Validate discussion number is numeric
        try:
            int(number)
        except ValueError:
            raise ValueError(f"Discussion number must be numeric: {number}")
            
        self.owner = owner
        self.repo = repo
        self.number = number

    @property
    def reference(self) -> str:
        """Returns the reference part of the RID: '<owner>/<repo>/<number>'."""
        return f"{self.owner}/{self.repo}/{self.number}"
    
    @property
    def repository_full_name(self) -> str:
        """Returns the full repository name: '<owner>/<repo>'."""
        return f"{self.owner}/{self.repo}"
    
    @property
    def html_url(self) -> str:
        """Returns the HTML URL to view this discussion on GitHub."""
        return f"https://github.com/{self.owner}/{self.repo}/discussions/{self.number}"
    
    @property
    def api_url(self) -> str:
        """Returns the GitHub API URL for this discussion (GraphQL)."""
        return f"https://api.github.com/graphql"  # GraphQL endpoint - would require a proper query

    @classmethod
    def from_reference(cls, reference: str) -> "GithubDiscussion":
        """
        Creates a GithubDiscussion instance from its reference string.
        
        Args:
            reference: String in format '<owner>/<repo>/<number>'
            
        Returns:
            GithubDiscussion instance
            
        Raises:
            ValueError: If the reference format is invalid
        """
        try:
            parts = reference.split("/", maxsplit=2)
            if len(parts) != 3:
                raise ValueError("Reference must contain exactly two '/' separators")
                
            owner, repo, number = parts
            
            if not owner or not repo or not number:
                raise ValueError("Owner, repo, and discussion number parts cannot be empty")
                
            # Validate discussion number is numeric
            try:
                int(number)
            except ValueError:
                raise ValueError(f"Discussion number must be numeric: {number}")
                
            return cls(owner=owner, repo=repo, number=number)
            
        except ValueError as e:
            raise ValueError(f"Invalid reference format for GithubDiscussion. Expected '<owner>/<repo>/<number>', got '{reference}'. Error: {e}") from e
        except Exception as e:
            raise TypeError(f"Unexpected error parsing GithubDiscussion reference '{reference}': {e}") from e


class GithubAction(ORN):
    """
    Resource Identifier (RID) for a GitHub Actions workflow run.
    
    Format: orn:github.action:<owner>/<repo>/<run_id>
    Example: orn:github.action:microsoft/vscode/12345678
    """
    namespace = "github.action"

    def __init__(self, owner: str, repo: str, run_id: str):
        """
        Initialize a GitHub Actions workflow run RID.
        
        Args:
            owner: The repository owner (user or organization)
            repo: The repository name
            run_id: The workflow run ID (as a string)
        """
        if not owner or not repo or not run_id:
            raise ValueError("Owner, repo, and run ID cannot be empty")
            
        if "/" in owner or "/" in repo:
            raise ValueError("Owner and repo cannot contain '/' character")
            
        # Validate run ID is numeric
        try:
            int(run_id)
        except ValueError:
            raise ValueError(f"Run ID must be numeric: {run_id}")
            
        self.owner = owner
        self.repo = repo
        self.run_id = run_id

    @property
    def reference(self) -> str:
        """Returns the reference part of the RID: '<owner>/<repo>/<run_id>'."""
        return f"{self.owner}/{self.repo}/{self.run_id}"
    
    @property
    def repository_full_name(self) -> str:
        """Returns the full repository name: '<owner>/<repo>'."""
        return f"{self.owner}/{self.repo}"
    
    @property
    def html_url(self) -> str:
        """Returns the HTML URL to view this workflow run on GitHub."""
        return f"https://github.com/{self.owner}/{self.repo}/actions/runs/{self.run_id}"
    
    @property
    def api_url(self) -> str:
        """Returns the GitHub API URL for this workflow run."""
        return f"https://api.github.com/repos/{self.owner}/{self.repo}/actions/runs/{self.run_id}"

    @classmethod
    def from_reference(cls, reference: str) -> "GithubAction":
        """
        Creates a GithubAction instance from its reference string.
        
        Args:
            reference: String in format '<owner>/<repo>/<run_id>'
            
        Returns:
            GithubAction instance
            
        Raises:
            ValueError: If the reference format is invalid
        """
        try:
            parts = reference.split("/", maxsplit=2)
            if len(parts) != 3:
                raise ValueError("Reference must contain exactly two '/' separators")
                
            owner, repo, run_id = parts
            
            if not owner or not repo or not run_id:
                raise ValueError("Owner, repo, and run ID parts cannot be empty")
                
            # Validate run ID is numeric
            try:
                int(run_id)
            except ValueError:
                raise ValueError(f"Run ID must be numeric: {run_id}")
                
            return cls(owner=owner, repo=repo, run_id=run_id)
            
        except ValueError as e:
            raise ValueError(f"Invalid reference format for GithubAction. Expected '<owner>/<repo>/<run_id>', got '{reference}'. Error: {e}") from e
        except Exception as e:
            raise TypeError(f"Unexpected error parsing GithubAction reference '{reference}': {e}") from e


class GithubGist(ORN):
    """
    Resource Identifier (RID) for a GitHub Gist.
    
    Format: orn:github.gist:<username>/<gist_id>
    Example: orn:github.gist:octocat/aa5a315d61ae9438b18d
    """
    namespace = "github.gist"

    def __init__(self, username: str, gist_id: str):
        """
        Initialize a GitHub Gist RID.
        
        Args:
            username: The owner of the gist
            gist_id: The gist ID
        """
        if not username or not gist_id:
            raise ValueError("Username and gist ID cannot be empty")
            
        if "/" in username or "/" in gist_id:
            raise ValueError("Username and gist ID cannot contain '/' character")
            
        self.username = username
        self.gist_id = gist_id

    @property
    def reference(self) -> str:
        """Returns the reference part of the RID: '<username>/<gist_id>'."""
        return f"{self.username}/{self.gist_id}"
    
    @property
    def html_url(self) -> str:
        """Returns the HTML URL to view this gist on GitHub."""
        return f"https://gist.github.com/{self.username}/{self.gist_id}"
    
    @property
    def api_url(self) -> str:
        """Returns the GitHub API URL for this gist."""
        return f"https://api.github.com/gists/{self.gist_id}"

    @classmethod
    def from_reference(cls, reference: str) -> "GithubGist":
        """
        Creates a GithubGist instance from its reference string.
        
        Args:
            reference: String in format '<username>/<gist_id>'
            
        Returns:
            GithubGist instance
            
        Raises:
            ValueError: If the reference format is invalid
        """
        try:
            parts = reference.split("/")
            if len(parts) != 2:
                raise ValueError("Reference must contain exactly one '/' separator")
                
            username, gist_id = parts
            
            if not username or not gist_id:
                raise ValueError("Username and gist ID parts cannot be empty")
                
            return cls(username=username, gist_id=gist_id)
            
        except ValueError as e:
            raise ValueError(f"Invalid reference format for GithubGist. Expected '<username>/<gist_id>', got '{reference}'. Error: {e}") from e
        except Exception as e:
            raise TypeError(f"Unexpected error parsing GithubGist reference '{reference}': {e}") from e