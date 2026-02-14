    use master
    go

    if exists ( Select 1 from sys.databases where [name] ='mlops_db')
    begin 
	    print '--- mlops_db found. dropping it now'
        alter database mlops_db set single_user with rollback immediate;
	    drop database mlops_db;
      
    end

    go
    print '--- Creating mlops_db database'
    create database mlops_db

    go
    use mlops_db;

    go
    print '--- Creating new file group t1_fg1 in mlops_db'
    alter database mlops_db add filegroup t1_fg1

    go
    print '--- Creating new file group t1_fg2 in mlops_db'
    alter database mlops_db add filegroup t1_fg2

    go
    print '--- Creating new file group t2_fg1 in mlops_db'
    alter database mlops_db add filegroup t2_fg1

    go
    print '--- Creating new file group t2_fg2 in mlops_db'
    alter database mlops_db add filegroup t2_fg2

    go
    print '--- Creating new file group t2_fg3 in mlops_db'
    alter database mlops_db add filegroup t2_fg3

    -- File group 1, data file 1/2, volume v1
    go
    print '--- Adding File group 1, data file 1/2, volume v1'
    alter database mlops_db add file (
        name = 'mlops_db_t1_fg1_file1',
        filename = '/user_data/v1/mlops_db_t1_fg1_f1.ndf',
        size = 5MB,
        filegrowth = 5MB
        ),
        (
        name = 'mlops_db_t1_fg1_file2',
        filename = '/user_data/v1/mlops_db_t1_fg1_f2.ndf',
        size = 5MB,
        filegrowth = 5MB
        ) To filegroup t1_fg1

    -- File group 2, data file 1/2/3, volume v2
    go
    print '--- File group 2, data file 1/2/3, volume v2'
    alter database mlops_db add file (
        name = 'mlops_db_t1_fg2_file1',
        filename = '/user_data/v2/mlops_db_t1_fg2_f1.ndf',
        size = 5MB,
        filegrowth = 5MB
        ),
        (
        name = 'mlops_db_t1_fg2_file2',
        filename = '/user_data/v2/mlops_db_t1_fg2_f2.ndf',
        size = 5MB,
        filegrowth = 5MB
        ),
        (
        name = 'mlops_db_t1_fg2_file3',
        filename = '/user_data/v2/mlops_db_t1_fg2_f3.ndf',
        size = 5MB,
        filegrowth = 5MB
        ) To filegroup t1_fg2


    -- File group 1, data file 1/2, volume v1
    go
    print '--- File group 1, data file 1/2, volume v1'
    alter database mlops_db add file (
        name = 'mlops_db_t2_fg1_file1',
        filename = '/user_data/v1/mlops_db_t2_fg1_f1.ndf',
        size = 5MB,
        filegrowth = 5MB
        ),
        (
        name = 'mlops_db_t2_fg1_file2',
        filename = '/user_data/v1/mlops_db_t2_fg1_f2.ndf',
        size = 5MB,
        filegrowth = 5MB
        ) To filegroup t2_fg1

    --  File group 2, data file 1/2, volume v3
    go
    print '---  File group 2, data file 1/2, volume v3'
    alter database mlops_db add file (
        name = 'mlops_db_t2_fg2_file1',
        filename = '/user_data/v3/mlops_db_t2_fg2_f1.ndf',
        size = 5MB,
        filegrowth = 5MB
        ),
        (
        name = 'mlops_db_t2_fg2_file2',
        filename = '/user_data/v3/mlops_db_t2_fg2_f2.ndf',
        size = 5MB,
        filegrowth = 5MB
        ) To filegroup t2_fg2

    -- File group 3, data file 1/2/3/4, volume v4
    go
    print '---  File group 3, data file 1/2/3/4, volume v4'
    alter database mlops_db add file (
        name = 'mlops_db_t2_fg3_file1',
        filename = '/user_data/v4/mlops_db_t2_fg3_f1.ndf',
        size = 5MB,
        filegrowth = 5MB
        ),
        (
        name = 'mlops_db_t2_fg3_file2',
        filename = '/user_data/v4/mlops_db_t2_fg3_f2.ndf',
        size = 5MB,
        filegrowth = 5MB
        ),
        (
        name = 'mlops_db_t2_fg3_file3',
        filename = '/user_data/v4/mlops_db_t2_fg3_f3.ndf',
        size = 5MB,
        filegrowth = 5MB
        ),
        (
        name = 'mlops_db_t2_fg3_file4',
        filename = '/user_data/v4/mlops_db_t2_fg3_f4.ndf',
        size = 5MB,
        filegrowth = 5MB
        ) To filegroup t2_fg3


    -- Creating partion for customer_status
    go
    print '--- Creating partion for customer_status'
    create partition function pf_customer_status (tinyint)
    As range left for values (0);

    -- Creating partion for vehicle_type
    go
    print '--- Creating partion for vehicle_type'
    create partition function pf_vehicle_type (tinyint)
    As range left for values (1, 2);

    -- Creating partion scheme for customer_status
    go
    print '--- Creating partion scheme for customer_status'
    create partition scheme ps_customer_status_partition
    as partition pf_customer_status
    to (t1_fg1, t1_fg2)

     -- Creating partion scheme for vehicle_type
    go
    print '--- Creating partion scheme for vehicle_type'
    create partition scheme ps_vehicle_type_partition
    as partition pf_vehicle_type
    to (t2_fg1, t2_fg2, t2_fg3)


    -- Creating table -> customers
    go
    print '--- Creating table -> customers'
    create table customers(
        id int identity(1,1),
        full_name nvarchar(100),
        is_paid tinyint not null,
        signup_date date,
        constraint pk_customers primary key (id, is_paid)
        ) on ps_customer_status_partition(is_paid)
    
    -- Creating table -> vehicles
    go
    print '--- Creating table -> vehicles'
    create table vehicles(
        id int identity(1,1),
        model_name nvarchar(100),
        vehicle_type_id tinyint not null,
        model_year int,
        constraint pk_vehicles primary key (id, vehicle_type_id)
        ) on ps_vehicle_type_partition(vehicle_type_id)

    -- Creating data into customers table
    go
    print '--- Creating data into customers table'
    insert into customers(full_name, is_paid, signup_date) values
    ('Bilal Rao', 0, '2025-01-05'),
    ('Ali Hassan', 0, '2025-02-01'),
    ('Ahmed Raza', 1, '2025-03-09'),
    ('Waris Ali', 0, '2025-04-15'),
    ('Baber Azam', 1, '2025-04-25'),
    ('Temor Beig', 0, '2025-05-15'),
    ('Rabia Sheikh', 1, '2025-01-15')

    -- Creating data into vehicles table
    go
    print '--- Creating data into vehicles table'
    insert into vehicles(model_name, vehicle_type_id, model_year) values
    ('Suzuki Swift', 1, 2022),
    ('Honda Civic', 1, 2023),
    ('Havel Phev', 2, 2025),
    ('Toyota Cros', 2, 2025),
    ('Byd Atto 3',3, 2026),
    ('Deepal S07',3, 2026),
    ('Byd Atto 4',3, 2027),
    ('Deepal S08',3, 2027)

    -- Valiating partitions for customers table
    go
    print '--- Valiating partitions for customers table'
    select 
        p.partition_number,
        p.rows,
        fg.name AS filegroup_name
    from sys.partitions p
    join sys.destination_data_spaces dds on p.partition_number = dds.destination_id
    join sys.partition_schemes ps on dds.partition_scheme_id = ps.data_space_id
    join sys.filegroups fg on dds.data_space_id = fg.data_space_id
    where p.object_id = object_id('customers')
    order by p.partition_number;

    -- Valiating partitions for vehicles table
    go
    print '--- Valiating partitions for vehicles table'
    select 
        p.partition_number,
        p.rows,
        fg.name AS filegroup_name
    from sys.partitions p
    join sys.destination_data_spaces dds on p.partition_number = dds.destination_id
    join sys.partition_schemes ps on dds.partition_scheme_id = ps.data_space_id
    join sys.filegroups fg on dds.data_space_id = fg.data_space_id
    where p.object_id = object_id('vehicles')
    order by p.partition_number;

    -- Valiating partitions wise data count for customers table
    go
    print '--- Valiating partitions wise data count for customers table'
    select case $partition.pf_customer_status(is_paid)
                when 1 then 'paid customer partition'
                when 2 Then 'un-paid customer partition'
            end as partition_name,
            count(*) as total_customers
    from customers
    group by $partition.pf_customer_status(is_paid)

    
    -- Valiating partitions wise data count for vehicles table
    go
    print '--- Valiating partitions wise data count for vehicles table'
    select case $partition.pf_vehicle_type(vehicle_type_id)
                when 1 then 'gasoline partition'
                when 2 Then 'hybrid partition'
                when 3 Then 'electric partition'
            end as partition_name,
            count(*) as total_vehicles
    from vehicles
    group by $partition.pf_vehicle_type(vehicle_type_id)
            