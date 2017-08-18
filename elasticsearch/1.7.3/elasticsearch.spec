%define __jar_repack 0
Name:           elasticsearch
Version:        1.7.3
Release:        2%{?dist}
Summary:        Elasticsearch is a distributed, RESTful search and analytics engine capable of solving a growing number of use cases.

License:        ASL 2.0
URL:            https://www.elastic.co/products/elasticsearch
Source0:        https://download.elastic.co/elasticsearch/release/org/elasticsearch/distribution/tar/elasticsearch/%{version}/%{name}-%{version}.tar.gz
Source1:        %{name}.service
Source2:        90-%{name}.conf
Source3:        %{name}

%description
Elasticsearch is a distributed, RESTful search and analytics engine capable of solving a growing number of use cases. As the heart of the Elastic Stack, it centrally stores your data so you can discover the expected and uncover the unexpected. 

%prep
%setup -q -n %{name}-%{version}

%install
rm -rf $RPM_BUILD_ROOT
# binary files
%{__mkdir} -p %{buildroot}/opt/%{name}/bin
%{__install} -p -m 755 bin/elasticsearch %{buildroot}/opt/%{name}/bin
%{__install} -p -m 644 bin/elasticsearch.in.sh %{buildroot}/opt/%{name}/bin
%{__install} -p -m 755 bin/plugin %{buildroot}/opt/%{name}/bin

# library files
%{__mkdir} -p %{buildroot}/opt/%{name}/lib
%{__mkdir} -p %{buildroot}/opt/%{name}/lib/sigar
%{__install} -p -m 644 lib/*.jar %{buildroot}/opt/%{name}/lib
%{__install} -p -m 644 lib/sigar/*.jar %{buildroot}/opt/%{name}/lib/sigar
%{__install} -p -m 644 lib/sigar/libsigar-amd64-linux.so %{buildroot}/opt/%{name}/lib/sigar
%{__install} -p -m 644 lib/sigar/libsigar-x86-linux.so %{buildroot}/opt/%{name}/lib/sigar
%{__install} -p -m 644 lib/sigar/libsigar-ia64-linux.so %{buildroot}/opt/%{name}/lib/sigar

# plugin dir
%{__mkdir} -p %{buildroot}/opt/%{name}/plugins

# config files & scripts
%{__mkdir} -p %{buildroot}%{_sysconfdir}/%{name}
%{__mkdir} -p %{buildroot}%{_sysconfdir}/%{name}/scripts
%{__install} -p -m 644 config/* %{buildroot}%{_sysconfdir}/%{name}

# service unit file
%{__mkdir} -p %{buildroot}%{_unitdir}
%{__install} -p -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/

# environment variables
%{__mkdir} -p %{buildroot}%{_sysctldir}
%{__install} -p -m 644 %{SOURCE2} %{buildroot}%{_sysctldir}/
%{__mkdir} -p %{buildroot}%{_localstatedir}/run/%{name}
%{__mkdir} -p %{buildroot}%{_sysconfdir}/sysconfig
%{__install} -p -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/elasticsearch

%files
%defattr(-,root,root,-)
%doc     README.textile NOTICE.txt
%license LICENSE.txt
/opt/%{name}/bin/*
/opt/%{name}/lib/*
/opt/%{name}/lib/sigar/*
%config(noreplace) %{_sysconfdir}/%{name}/*
%config(noreplace) %{_sysconfdir}/sysconfig/elasticsearch
%dir %{_sysconfdir}/%{name}/scripts
%{_unitdir}/elasticsearch.service
%{_sysctldir}/90-elasticsearch.conf
%dir %{_localstatedir}/run/%{name}

%changelog
* Fri Aug 18 2017  CentOS 7 Release Engineering <ngdocker@gmail.com> - 0.3.0
- Fix pid dir path.

* Thu Aug 17 2017  CentOS 7 Release Engineering <ngdocker@gmail.com> - 0.2.0
- Remove elasticsearch user/group in service unit file.

* Wed Aug 14 2017  CentOS 7 Release Engineering <ngdocker@gmail.com> - 0.1.0
- Initial package