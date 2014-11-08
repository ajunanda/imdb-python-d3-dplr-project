#### Create a local work repo & remote repo on Github

The very first step of setting up a project is to create a local work repository, also known as 'repo' in short. You can do this by simply typing `mkdir myLocalRepo` in the command line. In case your local machine has a failure, you can backup all your work in a remote work repository, hosted on a third party site like Github.com. Remember that github is free so all of your repos will be public and not proprietary.

Creating a remote repo on github is easy, follow the instructions [here]. Once the remote directory is set up, you can simply `git remote add origin https://github.com/robert8138/imdb_project.git` in your local work repo, this effectively will link your local working directory to the remote working directory. Anything that you add, modify on the local directory can be `push` to the remote repo by `git push`.

#### Setting up virtualenv

In my particular case, I knew I am going to write a scraper in Python, so upon setting up my local work directory, I didn't just use `mkdir`. Instead, I created a virtualenv directory by typing `virtualenv imdb_project`. The advantage of virtualenv is that pip is installed by default, so you can install all the python packages using `pip install`. Furthermore, it create a virtual environment where all the package management business is taken care of, so you don't need to worry about namespace collision.


[here]: https://help.github.com/articles/create-a-repo/