# -*- mode: ruby -*-
# vi: set ft=ruby :

LIST_OF_DB_ENGINE_SIGNIFIERS = ["postgresql", "mysql-server"]

DB_ENGINES = Array.new,

#default VARIABLES
VARIABLES = {
             "DB_NAME" => nil,
             "DB_USER" => nil,
             "DB_PASSWORD" => nil,}

PROJECTS = []

Vagrant.configure("2") do |config|
  puts "######################################################"
  puts "# MMVagrantfile Version: 1.3.1                       #"
  puts "# MMVagrantBox  Version: mm-debian-jessie-p36-v1.0.0 #"
  puts "######################################################"

  ######################
  #setup the base image#
  ######################

  config.vm.box = "mm-debian-jessie-p36-v1.0.0"
  config.vm.box_url = "http://s3.amazonaws.com/metametrics-dev/images/mm-debian-jessie-p36-v1.0.0.box"
  config.vm.synced_folder "../", "/home/vagrant/code"

  #Add ssh key forwarding
  config.ssh.forward_agent = true

  # Assign IP on a private network, box can be accessed from other boxes and from host.
  config.vm.network "private_network", type: "dhcp"

  #Add github to the known hosts
  config.vm.provision "shell", privileged: false, inline: <<-SHELL
      sudo ssh-keyscan -t rsa github.com | sudo tee /root/.ssh/known_hosts
      ssh-keyscan -t rsa github.com >> ~/.ssh/known_hosts
  SHELL

  # Add github to known hosts for root
  config.vm.provision "shell", inline: "mkdir -p /root/.ssh/ && touch /root/.ssh/known_hosts"
  config.vm.provision "shell", inline: "ssh-keyscan -t rsa github.com >> /root/.ssh/known_hosts"

  config.vm.provision "shell", inline: "sudo pip3.6 install -U setuptools"


  PROJECTS.push({
    'virtual_path' => File.join('code', File.basename(Dir.getwd)),
    'host_path' => '.',
    'environment_name' => 'environment'})


  ###############################
  #Do user specific provisioning#
  ###############################
  if File.file?(File.join(ENV['HOME'], "/vagrant_global.sh"))
    config.vm.provision :shell, path: File.join(ENV['HOME'], "/vagrant_global.sh"), env: VARIABLES
  else
    config.vm.provision "shell", inline: "echo 'You can create a vagrant_global.sh shell script file located in your home directory to create settings across all of your vagrant vms.'"
  end


  ###########################
  # Provision for project/s #
  ###########################

  for project in PROJECTS
    setup_ports(config)
    install_dependencies(config, project)
    load_environment_variables_from_file(config, project)
    setup_databases(config)
    pip_install_requirements(config, project)
    provision_local_dev(config, project)
  end
end


#####################
# Helper Functions  #
#####################

def provision_local_dev(config, project_data)
    local_dev_script = File.join(project_data['host_path'], "vagrant_local.sh")
    if File.file?(local_dev_script)
        config.vm.provision "shell", inline: "echo 'HELLO!'"
        config.vm.provision :shell, path: local_dev_script, env: VARIABLES
    else
    config.vm.provision "shell", inline: "echo 'You can create a vagrant_local.sh shell script file located in this directory to create settings specific to this vagrant vm.'"
    end

    local_dev_module = File.join(project_data['host_path'], "vagrant_local.rb")
    if File.file?(local_dev_module)
      require_relative './vagrant_local'

      include VagrantLocal
      provision(config, project_data)
    else
      config.vm.provision "shell", inline: "echo 'You can create a vagrant_local.sh shell script file located in this directory to create settings specific to this vagrant vm.'"
    end
end


def setup_ports config
  if not File.file?("PORTS")
    #since we dont have a PORTS file, no ports are created
    config.vm.provision "shell", inline: "echo 'You can create multiple ports to access the vagrantbox by creating a PORTS file in this directory.'"
    return
  end

  ports_data = IO.foreach("PORTS")

  ports_data.each {|port_data|
    #remove comments
    port_data_cleaned = port_data.split("#")[0].strip
    if port_data_cleaned == ""
      next
    end

    #make sure we have all 3 fields (name, guest, host)
    port_data_list = port_data_cleaned.split(",")
    if port_data_list.length != 3
      puts "Not correct number of parameters for port: " + port_data_list[0]
      next
    end

    VARIABLES[port_data_list[0]+"_GUEST_PORT"] = port_data_list[1]
    VARIABLES[port_data_list[0]+"_HOST_PORT"] = port_data_list[2]

    config.vm.network "forwarded_port", guest: (port_data_list[1]).to_i, host: (port_data_list[2]).to_i
  }

end

def is_python3 path
    dependency_file_location = File.join(path, 'DEPENDENCIES')
    File.foreach(dependency_file_location).flat_map { |e|
        if e.strip.include? 'python3'
            return true
        end
    }
    return false
end


def install_dependencies(config, project_data)
# Upgrade pip3 to avoid requests bug

  deps_path = File.join(project_data['host_path'], 'DEPENDENCIES')
  deps = File.foreach(deps_path).flat_map { |e| [e.chomp.strip] }
  deps = deps.join(" ")
  config.vm.provision "shell", inline: "sudo apt-get update"
  config.vm.provision "shell", inline: "export DEBIAN_FRONTEND=noninteractive; sudo -E apt-get install %s screen -y" % deps

  deps.split(" ").each {|dependency|
    if LIST_OF_DB_ENGINE_SIGNIFIERS.include?(dependency.strip)
      raise 'Do not put database specific information in DEPENDENCIES. Create/Use DEV_DEPENDENCIES for development databases.'
    end
  }
  dev_deps_path = File.join(project_data['host_path'], 'DEV_DEPENDENCIES')
  if File.file?(dev_deps_path)
    dev_deps = File.foreach(dev_deps_path).flat_map { |e| [e.chomp.strip] }
    dev_deps = dev_deps.join(" ")
    config.vm.provision "shell", inline: "export DEBIAN_FRONTEND=noninteractive; sudo -E apt-get install %s screen -y" % dev_deps

    # Store the db that we are using#
    dev_deps.split(" ").each {|dependency|
      if LIST_OF_DB_ENGINE_SIGNIFIERS.include?(dependency.strip)
        DB_ENGINES.push(dependency.strip)
      end
    }

  else
    config.vm.provision "shell", inline: "echo 'You can create a DEV_DEPENDENCIES file which houses dependancies specific to a dev environment and not needed in production. For example mysql or postgres, to run on the dev machine, but production would use a different server for the database.'"
  end
end

def pip_install_requirements(config, project_data)
    requirements_path = File.join(project_data['virtual_path'], 'requirements.txt')

    python_type, pip_type = 'python3.6', 'pip3.6'
    config.vm.provision "shell", inline: "sudo pip3.6 install --upgrade pip==18.1"
    # Maybe this should be in the base image
    config.vm.provision "shell", inline: "sudo pip3.6 install envs[cli]==1.3"
    config.vm.provision "shell", inline: "%s install -r %s --process-dependency-links" % [pip_type, requirements_path]
end


def setup_postgres config
  # builds the postgres database
  config.vm.provision "shell", inline: "sudo -u postgres psql -c \"select 1 from pg_roles where rolname='"+ VARIABLES['DB_USER']+"'\" | grep -q 1 || sudo -u postgres psql -c \"CREATE USER "+ VARIABLES['DB_USER'] +" WITH PASSWORD '"+ VARIABLES['DB_PASSWORD'] +"' CREATEDB;\""

  config.vm.provision "shell", privileged: false, inline: "psql -lqt | grep -wq '"+ VARIABLES['DB_NAME'] +"' || createdb "+ VARIABLES['DB_NAME']
end

def setup_mysql config
  # build the mysql database
  config.vm.provision "shell",
      inline: "mysqladmin -uroot password vagrant;
               mysql -uroot -pvagrant -sse \"SELECT EXISTS(SELECT 1 FROM mysql.user WHERE user = '"+ VARIABLES['DB_USER']+"')\" | grep -q 1 || mysql -uroot -pvagrant -e \"CREATE USER '"+VARIABLES['DB_USER']+"'@'localhost' IDENTIFIED BY '"+VARIABLES['DB_PASSWORD']+"'\";
               mysql -uroot -pvagrant -e \"GRANT ALL PRIVILEGES ON *.* TO '"+VARIABLES['DB_USER']+"'@'localhost';\";
               mysql -u"+VARIABLES['DB_USER']+" -p"+VARIABLES['DB_PASSWORD']+" -e \"create database if not exists "+ VARIABLES['DB_NAME'] +";\"
               "
end

def setup_databases config
  #builds all the databases that we need based on the DEPENDENCIES file
  if not VARIABLES["DB_NAME"] or not VARIABLES["DB_PASSWORD"] or not VARIABLES["DB_USER"]
    #this breaks out since we dont have all the information needed
    return
  end

  #I decided to hardcode these if statements because there is only 2 maybe 3
  # much easier than the number of variables for it to do it using dictionaries
  DB_ENGINES.each {|db_engine|
    if db_engine == "postgresql"
      setup_postgres config
    end
    if db_engine == "mysql-server"
      setup_mysql config
    end
  }
end


###################################################################
# This function will iterate over all the data in the .env file
# it calls handle_environment_variable to do any special handling
#   for individual environment VARIABLES
###################################################################
def load_environment_variables_from_file(config, project_data)
  env_path = File.join(project_data['host_path'], '.env')

  if File.file?(env_path)
    envs = IO.foreach(env_path)
    envs.each {|env|
      env = env.strip

      #split on the [=].
    # get the name [0]
    # get the value [1]
    name = env.split("=").first
    value = env.split("=").last
      VARIABLES[name] = value
    }
    config.vm.provision "shell", inline: "if [ $(grep -c 'export $p' /home/vagrant/.profile) -lt 1 ]; then echo -e 'while read p; do\n  export $p\ndone < ~/"+project_data['virtual_path']+"/.env' >> /home/vagrant/.profile; fi"
  else
      config.vm.provision "shell", inline: "echo 'You are missing a .env file with enviroment variables. This may cause issues with your environment.'"
  end


end
