# Copyright 2019 Nokia
  
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
Name:		distributed-state-server
Version:	%{_version}
Release:	1%{?dist}
Summary:	Distributed State Server
Group:          %{_platform_group}
License:        %{_platform_license}
Source0:        %{name}-%{version}.tar.gz
Vendor:         %{_platform_vendor}

BuildArch:      noarch

BuildRequires: python
BuildRequires: python-setuptools

Requires: etcd
Requires: python2-python-etcd
Requires: python-dns


%description
This RPM contains source code for the distributed state server and its plugins

%prep
%autosetup

%install
mkdir -p %{buildroot}/%{_python_site_packages_path}/dss
mkdir -p %{buildroot}/opt/dss-server/plugins
cd src && python setup.py install --root %{buildroot} --no-compile --install-purelib %{_python_site_packages_path} --install-scripts %{_platform_bin_path} && cd -

cp plugins/*.py %{buildroot}/opt/dss-server/plugins/


%files
%{_python_site_packages_path}/dss*
%{_python_site_packages_path}/dss*
%{_platform_bin_path}/dsscli
%{_platform_bin_path}/dss
/opt/dss-server/plugins/*.py*

%pre

%post
echo "distributed-state-server succesfully installed"


%preun

%postun

%clean
rm -rf %{buildroot}
