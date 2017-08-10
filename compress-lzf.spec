%{?scl:%scl_package compress-lzf}
%{!?scl:%global pkg_name %{name}}

Name:		%{?scl_prefix}compress-lzf
Version:	1.0.3
Release:	7%{?dist}
Summary:	Basic LZF codec, compatible with standard C LZF package
License:	ASL 2.0
URL:		https://github.com/ning/compress
Source0:	https://github.com/ning/compress/archive/%{pkg_name}-%{version}.tar.gz

BuildRequires:	%{?scl_prefix_maven}maven-local
BuildRequires:	%{?scl_prefix_maven}mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:	%{?scl_prefix_maven}mvn(org.apache.maven.plugins:maven-enforcer-plugin)
BuildRequires:	%{?scl_prefix_maven}mvn(org.apache.maven.surefire:surefire-testng)
BuildRequires:	%{?scl_prefix_maven}mvn(org.sonatype.oss:oss-parent:pom:)
BuildRequires:	%{?scl_prefix_java_common}junit
BuildRequires:  %{?scl_prefix}snakeyaml
%{?scl:Requires: %scl_runtime}

BuildArch:	noarch

%description
Compression codec for LZF encoding for particularly encoding/decoding,
with reasonable compression. Compressor is basic Lempel-Ziv codec,
without Huffman (deflate/gzip) or statistical post-encoding. See
"http://oldhome.schmorp.de/marc/liblzf.html" for more on
original LZF package.

%package javadoc
Summary:	Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n compress-%{pkg_name}-%{version}

find . -name "*.class" -print -delete
find . -name "*.jar" -type f -print -delete

%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%pom_remove_plugin :maven-source-plugin
%pom_xpath_remove "pom:project/pom:build/pom:plugins/pom:plugin[pom:artifactId='maven-javadoc-plugin']/pom:executions"

%pom_add_dep junit:junit::test

%mvn_file : %{pkg_name}
%{?scl:EOF}

%build
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%mvn_build -- -Poffline-testing
%{?scl:EOF}

%install
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%mvn_install
%{?scl:EOF}

%files -f .mfiles
%doc README.md VERSION.txt
%license LICENSE

%files javadoc -f .mfiles-javadoc
%license LICENSE

%changelog
* Wed Oct 12 2016 Tomas Repik <trepik@redhat.com> - 1.0.3-7
- use standard SCL macros

* Wed Jul 27 2016 Tomas Repik <trepik@redhat.com> - 1.0.3-6
- scl conversion

* Tue Jun 21 2016 gil cattaneo <puntogil@libero.it> 1.0.3-5
- add missing build requires

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jan 30 2015 gil cattaneo <puntogil@libero.it> 1.0.3-2
- introduce license macro

* Mon Nov 03 2014 gil cattaneo <puntogil@libero.it> 1.0.3-1
- update to 1.0.3

* Wed Jul 02 2014 gil cattaneo <puntogil@libero.it> 0.9.8-3
- fix SUID issue in LZF compression rhbz#1115264

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Aug 14 2013 gil cattaneo <puntogil@libero.it> 0.9.8-1
- initial rpm
