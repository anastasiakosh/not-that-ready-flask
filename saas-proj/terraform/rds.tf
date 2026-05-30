resource "aws_security_group" "rds_sg" {
  name        = "commerce_rds_sg"
  description = "Allow inbound traffic from EKS"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = [module.vpc.vpc_cidr_block]
  }
}

resource "aws_db_instance" "postgres" {
  identifier           = "commerce-db"
  engine               = "postgres"
  engine_version       = "15.3"
  instance_class       = "db.t3.micro"
  allocated_storage    = 20
  
  db_name              = "commercedb"
  username             = "admin"
  password             = "SuperSecretPassword123!" 
  
  db_subnet_group_name   = module.vpc.database_subnet_group
  vpc_security_group_ids = [aws_security_group.rds_sg.id]
  
  skip_final_snapshot  = true
  publicly_accessible  = false
}
