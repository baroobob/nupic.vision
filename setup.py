# ----------------------------------------------------------------------
# Numenta Platform for Intelligent Computing (NuPIC)
# Copyright (C) 2016-2017, Numenta, Inc.  Unless you have an agreement
# with Numenta, Inc., for a separate license for this software code, the
# following terms and conditions apply:
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero Public License for more details.
#
# You should have received a copy of the GNU Affero Public License
# along with this program.  If not, see http://www.gnu.org/licenses.
#
# http://numenta.org/licenses/
# ----------------------------------------------------------------------

"""Vision tools and experiments for NuPIC.

The ImageSensor was originally part of the main NuPIC repository and
has been moved here with other image and vision components and
experiments to reduce the dependencies for NuPIC users that aren't
doing vision-related work.
"""

import os
import pkg_resources
from setuptools import setup, find_packages
import subprocess

REPO_DIR = os.path.dirname(os.path.realpath(__file__))


def _getPrereleasePackages():
  skipPkgs = []

  try:
    nupicDist = pkg_resources.get_distribution("nupic")
    if pkg_resources.parse_version(nupicDist.version).is_prerelease:
      skipPkgs.append("nupic")
  except pkg_resources.DistributionNotFound:
    pass

  try:
    pkg_resources.get_distribution("htmresearch")
    skipPkgs.append("htmresearch")
  except pkg_resources.DistributionNotFound:
    pass

  return skipPkgs


def getRequirements():
  skipPkgs = _getPrereleasePackages()
  reqs = []
  with open(os.path.join(REPO_DIR, "requirements.txt")) as requirementsFile:
    for req in requirementsFile.readlines():
      if req.strip().split("=")[0] not in skipPkgs:
        reqs.append(req.strip())
  return reqs


def getVersion():
  with open(os.path.join(REPO_DIR, "VERSION")) as versionFile:
    return versionFile.read().strip()


def buildMnistCpp():
  cwd = os.getcwd()
  workDir = os.path.join(os.path.dirname(__file__),
                         "src/nupic/vision/mnist/data")
  os.chdir(workDir)
  try:
    subprocess.check_call("./build.sh", shell=True)
  finally:
    os.chdir(cwd)


buildMnistCpp()


setup(
    name="nupic.vision",
    version=getVersion(),
    description=__doc__,
    install_requires=getRequirements(),
    package_dir={"": "src"},
    packages=find_packages("src"),
    namespace_packages=["nupic"],
    package_data={
        "nupic.vision.data": ["*.jpg", "*.xml"],
        "nupic.vision.mnist.data": ["extract_mnist"],
    },
    zip_safe=False,
)
