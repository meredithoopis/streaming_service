config = {
    "kafka": {
        "sasl.username": "confluent_api_key", 
        "sasl.password": "confluent_secret_key", 
        "bootstrap.servers": "confluent_server", 
        'security.protocol': 'SASL_SSL', 
        'sasl.mechanisms': 'PLAIN', 
        'session.timeout.ms': 50000
    }, 
    "schema_registry": {
        "url": "confluent_link_schema_registry", 
        "basic.auth.user.info": "api_key_for_schema_registry:secret_key_for_schema_registry"
    }
}