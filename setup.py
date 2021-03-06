from setuptools import setup

setup(name="chefpy",
      version="0.321",
      description="Unofficial Codechef Api for user's status,rank,solutions etc.",
      url="http://github.com/prdpx7/chefpy",
      author="Pradeep Khileri",
      author_email="pradeepchoudhary009@gmail.com",
      license="MIT",
      packages=["chefpy"],
      scripts=["./bin/chefpy"],
      keywords='api codechef automation command-line linux web-scraping',
      install_requires=[
          "bs4",
          "requests",
      ],
      zip_safe=False)

