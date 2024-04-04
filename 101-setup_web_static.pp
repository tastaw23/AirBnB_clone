# Ensure Nginx is installed
package { 'nginx':
  ensure => installed,
}

# Create necessary directories
file { '/data':
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

file { '/data/web_static':
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

file { '/data/web_static/releases':
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

file { '/data/web_static/shared':
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

file { '/data/web_static/releases/test':
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

# Create fake HTML file
file { '/data/web_static/releases/test/index.html':
  ensure  => present,
  content => '<html>\n  <head>\n  </head>\n  <body>\n    Holberton School\n  </body>\n</html>\n',
  owner   => 'ubuntu',
  group   => 'ubuntu',
}

# Create symbolic link
file { '/data/web_static/current':
  ensure => link,
  target => '/data/web_static/releases/test',
  owner  => 'root',
  group  => 'root',
}

# Configure Nginx to serve content
file { '/etc/nginx/sites-available/default':
  ensure  => file,
  content => "
server {
    listen 80 default_server;
    listen [::]:80 default_server;

    root /var/www/html;

    index index.html index.htm index.nginx-debian.html;

    server_name _;

    location /hbnb_static/ {
        alias /data/web_static/current/;
        index index.html;
    }
}
  ",
  require => Package['nginx'],
}

# Restart Nginx
service { 'nginx':
  ensure    => running,
  enable    => true,
  subscribe => File['/etc/nginx/sites-available/default'],
}
