Name:		argo-probe-eudat-b2share
Version:	2.3
Release:	1%{?dist}
Summary:	Monitoring scripts that check the functionalities of B2SHAR (v2 + v3/RDM)
License:	GPLv3+
Packager:	Themis Zamani <themiszamani@gmail.com>

Source:		%{name}-%{version}.tar.gz
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}
AutoReqProv:    no
Requires:	python3
Requires:	python3-requests
Requires: 	python-jsonschema

%description
Nagios probe to check functionality and availability of B2SHARE service
(compatible with both legacy B2SHARE v2 and Invenio-RDM based B2SHARE v3).
The unified probe performs:
- search and record retrieval
- schema retrieval and metadata validation (Draft-04 for v2, Draft-07 for v3)
- robust handling of RDM vocabulary enrichments (default ignores vocab keys)
- file-bucket access and HEAD request on a file


Additional B2SHARE v3 options:
- --debug-metadata       : log stripped vocabulary keys (non-strict mode)
- --metadata-report      : print a summary of vocabulary-like keys

%prep
%setup -q

%define _unpackaged_files_terminate_build 0

%install
install -d %{buildroot}/%{_libexecdir}/argo/probes/eudat-b2share
install -m 755 check_b2share.py %{buildroot}/%{_libexecdir}/argo/probes/eudat-b2share/check_b2share.py

%files
%dir /%{_libexecdir}/argo
%dir /%{_libexecdir}/argo/probes/
%dir /%{_libexecdir}/argo/probes/eudat-b2share

%attr(0755,root,root) /%{_libexecdir}/argo/probes/eudat-b2share/check_b2share.py

%changelog

* Wed Aug 12 2026 Petri Laihonen <petri.laihonen@csc.fi> - 2.3-1
- Skip access-restricted and file-less records when selecting a record to probe
- Filter search to open records server-side (access_status=open) as defense-in-depth

* Fri Feb 11 2026 Petri Laihonen <petri.laihonen@csc.fi> - 2.2-1
- Remove --strict-metadata option
- Update README

* Fri Feb 06 2026 Petri Laihonen <petri.laihonen@csc.fi> - 2.1-1
- Add --strict-metadata, --debug-metadata, and --metadata-report options
- Preserve legacy filename and output/verbosity semantics

* Wed Feb 04 2026 Petri Laihonen <petri.laihonen@csc.fi> - 2.0-1
- Changes in order to probe RDM-based B2SHARE application.
- Added verbosity enhancements and updated timeout help text.
- Both, B2SHARE v2 and v3 (Release 3.0.2 and above) are now supported.

* Tue Nov 04 2025 Themis Zamani <themiszamani@gmail.com> - 0.8.1
- Minor updates to url check

* Fri Apr 05 2024 Giacomo Furlan   <giacomo.furlan@csc.fi> - 0.2.1
- Update python to 3.9
- Update requirements and dependencies
- Remove validator dependency

* Mon Mar 14 2022 Themis Zamani <themiszamani@gmail.com> - 0.5
- Update package prerequisites based on argo monitoring.

* Tue Nov 27 2018 Themis Zamani  <themiszamani@gmail.com> - 0.1-1
- Initial version of the package.

* Tue Nov 27 2018 Harri Hirvonsalo   <harri.hirvonsalo@csc.fi> - 0.1-1
- Initial version of the package.
