server {
    listen 80;
    server_name thepanipathandloom.com;

    return 301 https://$server_name$request_uri;
}

server {
    listen 80 default_server;
    server_name _;

    return 404;
}

server {
    server_name www.thepanipathandloom.com;

    # Redirect to non-www domain
    return 301 https://thepanipathandloom.com$request_uri;
}

server {
    listen 443 ssl;
    server_name thepanipathandloom.com;

    # SSL configurations
    ssl_certificate /etc/letsencrypt/live/thepanipathandloom.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/thepanipathandloom.com/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    #location = https://thepanipathandloom.com/category/Blinds%20For%20Windows/ {
    #    return 301 https://thepanipathandloom.com/category/blinds-for-windows/;
    #}

    # Permanent redirects
    rewrite https://thepanipathandloom.com/category/Blinds%20For%20Windows/$ https://thepanipathandloom.com/category/blinds-for-windows/ 301;
    # rewrite ^/category/CurtainsFabric/$ /category/curtainsfabric/ permanent;
    # rewrite ^/category/Mosquito%20Mesh/$ /category/mosquito-mesh/ permanent;
    # rewrite ^/category/Wallpapers/$ /category/wallpapers/ permanent;
    # rewrite ^/category/Panel/$ /category/panel/ permanent;
    # rewrite ^/category/Mattresses/$ /category/mattresses/ permanent;
    # rewrite ^/category/Fabric%20Use%20in%20Upholstery/$ /category/fabric-use-in-upholstery/ permanent;
    # rewrite ^/category/Product%20Use%20for%20Upholstery/$ /category/product-use-for-upholstery/ permanent;
    # rewrite ^/category/Interior/$ /category/interior/ permanent;
    # rewrite ^/category/Exterior%20Floor%20&%20Upholstery/$ /category/exterior-floor-upholstery/ permanent;
    # rewrite ^/category/Pergola/$ /category/pergola/ permanent;
    # rewrite ^/category/Special%20Blinds/$ /category/special-blinds/ permanent;


    # Proxy configurations for your backend
    location / {
        include proxy_params;
        proxy_pass http://unix:/python/panipat-deploy/ecomproj.sock;
        client_max_body_size 200M;
      }

}

