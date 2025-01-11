
# Run the tests
python -m pytest tests

# Check if the tests were successful
if [ $? -eq 0 ]
then
  echo "Tests passed, starting the server..."
  exec gunicorn -b :8080 app:app  # PROJECT-ID:REGION:INSTANCE-ID
else
  echo "Tests failed, not starting the server."
  exit 1
fi
