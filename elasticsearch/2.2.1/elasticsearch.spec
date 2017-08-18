%define __jar_repack 0
Name:           elasticsearch
Version:        2.2.1
Release:        3%{?dist}
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
%{__mkdir} -p %{buildroot}/opt/%{name}/bin
%{__install} -p -m 755 bin/elasticsearch %{buildroot}/opt/%{name}/bin
%{__install} -p -m 644 bin/elasticsearch.in.sh %{buildroot}/opt/%{name}/bin
%{__install} -p -m 755 bin/plugin %{buildroot}/opt/%{name}/bin
%{__mkdir} -p %{buildroot}/opt/%{name}/lib
%{__install} -p -m 644 lib/* %{buildroot}/opt/%{name}/lib
%{__mkdir} -p %{buildroot}/opt/%{name}/plugins
%{__mkdir} -p %{buildroot}/opt/%{name}/modules/lang-expression
%{__mkdir} -p %{buildroot}/opt/%{name}/modules/lang-groovy
%{__install} -p -m 644 modules/lang-expression/* %{buildroot}/opt/%{name}/modules/lang-expression
%{__install} -p -m 644 modules/lang-groovy/* %{buildroot}/opt/%{name}/modules/lang-groovy
%{__mkdir} -p %{buildroot}%{_sysconfdir}/%{name}
%{__mkdir} -p %{buildroot}%{_sysconfdir}/%{name}/scripts
%{__install} -p -m 644 config/* %{buildroot}%{_sysconfdir}/%{name}
%{__mkdir} -p %{buildroot}%{_unitdir}
%{__install} -p -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/
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
/opt/%{name}/modules/lang-expression/*
/opt/%{name}/modules/lang-groovy/*
%config(noreplace) %{_sysconfdir}/%{name}/*
%config(noreplace) %{_sysconfdir}/sysconfig/elasticsearch
%dir %{_sysconfdir}/%{name}/scripts
%{_unitdir}/elasticsearch.service
%{_sysctldir}/90-elasticsearch.conf
%dir %{_localstatedir}/run/%{name}

%post
if ! getent group elasticsearch > /dev/null; then
    groupadd -r elasticsearch
fi

if ! getent passwd elasticsearch > /dev/null; then
    useradd -r -g elasticsearch -d /opt/%{name} -s /sbin/nologin -c "You know, for search" elasticsearch
fi

chown root:elasticsearch %{_sysconfdir}/%{name}
chown -R elasticsearch:elasticsearch %{_sysconfdir}/%{name}/*
chown elasticsearch:elasticsearch %{_localstatedir}/run/%{name}
chown -R elasticsearch:elasticsearch /opt/%{name}/plugins


%changelog
* Fri Aug 18 2017  CentOS 7 Release Engineering <ngdocker@gmail.com> - 0.5.0
- Fix pid dir path.

* Thu Aug 17 2017  CentOS 7 Release Engineering <ngdocker@gmail.com> - 0.4.0
- Fix elasticsearch default properties.

* Tue Aug 15 2017  CentOS 7 Release Engineering <ngdocker@gmail.com> - 0.3.0
- Remove elasticsearch user/group in service unit file.

* Fri Aug 11 2017  CentOS 7 Release Engineering <ngdocker@gmail.com> - 0.2.0
- Add systemd service unit file, set vm.max_map_count to 262144

* Wed Aug 2 2017  CentOS 7 Release Engineering <ngdocker@gmail.com> - 0.1.0
- Initial package