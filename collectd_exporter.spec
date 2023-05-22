Name:           collectd_exporter
Version:        0.0.6
Release:        1%{?dist}
Summary:        Prometheus exporter for collectd data.

License:        GPLv3
URL:		https://github.com/prometheus/collectd_exporter/archive/refs/heads/master.tar.gz
Source0:        %{name}-%{version}.tar.gz
Source1:	%{name}.service
Source2:	%{name}.xml

BuildRequires:  golang
BuildRequires:  systemd-rpm-macros

Provides:       %{name} = %{version}

%description
An exporter for collectd. It accepts collectd's binary network protocol as sent by collectd's network
plugin and metrics in JSON format via HTTP POST as sent by collectd's write_http plugin, and transforms 
and exposes them for consumption by Prometheus.

%global debug_package %{nil}

%prep
curl -L %{url} -o %{name}-%{version}.tar.gz
rm -rf %{name}-%{version}
mkdir -p %{name}-%{version}
cd %{name}-%{version}
gzip -dc ../%{name}-%{version}.tar.gz |tar --strip-components 1 -xof -


%build
cd %{name}-%{version}
go build -v -o %{name}


%install
cd %{name}-%{version}
install -Dpm 0755 %{name} %{buildroot}%{_bindir}/%{name}
install -Dpm 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
install -Dpm 644 %{SOURCE2} %{buildroot}%{_prefix}/lib/firewalld/services/%{name}.xml

%check
# go test should be here... :)

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%files
%{_bindir}/%{name}
%{_unitdir}/%{name}.service
%{_prefix}/lib/firewalld/services/%{name}.xml


%changelog
* Wed May 22 2021 Patrik Pira - 0.0.6-1
- First release%changelog
