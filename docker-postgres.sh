docker run -p 5432:5432 -d \
	-e POSTGRES_USER="student" \
	-e POSTGRES_PASSWORD="student" \
	-e POSTGRES_DB="studentdb" \
	-v ${PWD}/data:/var/lib/postgresql/data \
	--name pg-container \
	postgres
