PATH = "k8s-in-gcp-terraform-ansible"
cmd = os.popen('cat <terra-dir>/terraform.tfstate.backup | jq .resources[].instances[].attributes.network_interface | grep -v null | jq .[].access_config[].nat_ip | sed -e \'s/"//g\' > PATH/gcp-nodes-ip.txt')

ips=[]
with open('PATH/gcp-nodes-ip.txt') as mh:
    ipl=mh.readlines()
    for l in ipl:
        ips.append(l)
print(ips)

with open('PATH/hosts') as g_ip:
    for line in g_ip.readlines():
        with open('$PATH/hosts1', 'a') as h_ip:
            #print(line)
            if line.startswith('master ansible_host'):
                line1 = 'master ansible_host='+ips[0].strip()+' ansible_user=ubuntu\n'
            elif line.startswith('worker1 ansible_host'):
                line2 = 'worker1 ansible_host=' + ips[1].strip() + ' ansible_user=ubuntu\n'
            elif line.startswith('worker2 ansible_host'):
                line3 = 'worker2 ansible_host=' + ips[2].strip() + ' ansible_user=ubuntu\n'
            else:
                print(line)

with open('PATH/hosts', 'w+') as u_ip:
    u_ip.write('[masters]\n')
    u_ip.write(line1)
    u_ip.write('[workers]\n')
    u_ip.write(line2)
    u_ip.write(line3)
    u_ip.write('[all:vars]\n')
    u_ip.write('ansible_python_interpreter = /usr/bin/python3\n')

cmd = subprocess.Popen('ansible-playbook -i hosts PATH/non-root-user.yml', stdout=subprocess.PIPE, shell=True)
c = str(cmd.communicate())
f = re.findall(r'successfully', c)
cmd = subprocess.Popen('ansible-playbook -i hosts PATH/kube-dependencies.yml', stdout=subprocess.PIPE, shell=True)
c = str(cmd.communicate())
f = re.findall(r'successfully', c)
cmd = subprocess.Popen('ansible-playbook -i hosts PATH/master-cluster.yml', stdout=subprocess.PIPE, shell=True)
c = str(cmd.communicate())
f = re.findall(r'successfully', c)
cmd = subprocess.Popen('ansible-playbook -i hosts PATH/workers-cluster.yml', stdout=subprocess.PIPE, shell=True)
c = str(cmd.communicate())
f = re.findall(r'successfully', c)


