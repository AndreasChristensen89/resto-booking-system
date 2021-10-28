command used for copying authentication templates to directory. Once copied we can make changes to the styling, and the content
cp -r ../.pip-modules/lib/python3.8/site-packages/allauth/templates/* ./templates

28/10/2021 - for some reason Django logs user out when following link to reservation_detail.html.
Console displays: "POST /accounts/logout/ HTTP/1.1" 302 0