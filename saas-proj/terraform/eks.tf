module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 19.0"

  cluster_name    = "commerance-eks-cluster" 
  cluster_version = "1.28"

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  eks_managed_node_groups = {
    app_nodes = {
      min_size     = 2
      max_size     = 5 
      desired_size = 2

      instance_types = ["t3.medium"]
      capacity_type = "ON_DEMAND"
    }
  }

  tags = {
    Environment = "production"
  }
}
