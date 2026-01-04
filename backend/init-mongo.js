// MongoDB initialization script
db = db.getSiblingDB('drobea');

// Create collections with validation
db.createCollection('users', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: ['username', 'email', 'password_hash'],
      properties: {
        username: { bsonType: 'string', minLength: 3, maxLength: 50 },
        email: { bsonType: 'string', pattern: '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$' },
        password_hash: { bsonType: 'string' },
        is_active: { bsonType: 'bool' },
        is_verified: { bsonType: 'bool' },
        created_at: { bsonType: 'date' },
        updated_at: { bsonType: 'date' }
      }
    }
  }
});

db.createCollection('wardrobe_items', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: ['user_id', 'name', 'category', 'image_url'],
      properties: {
        user_id: { bsonType: 'objectId' },
        name: { bsonType: 'string', minLength: 1, maxLength: 100 },
        category: { bsonType: 'string' },
        image_url: { bsonType: 'string' },
        created_at: { bsonType: 'date' },
        updated_at: { bsonType: 'date' }
      }
    }
  }
});

db.createCollection('outfits', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: ['user_id', 'name', 'items'],
      properties: {
        user_id: { bsonType: 'objectId' },
        name: { bsonType: 'string', minLength: 1, maxLength: 100 },
        items: { bsonType: 'array' },
        created_at: { bsonType: 'date' },
        updated_at: { bsonType: 'date' }
      }
    }
  }
});

db.createCollection('virtual_tryons', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: ['user_id', 'reference_image_url', 'garment_image_url'],
      properties: {
        user_id: { bsonType: 'objectId' },
        reference_image_url: { bsonType: 'string' },
        garment_image_url: { bsonType: 'string' },
        result_image_url: { bsonType: 'string' },
        created_at: { bsonType: 'date' },
        updated_at: { bsonType: 'date' }
      }
    }
  }
});

// Create indexes for better performance
db.users.createIndex({ 'email': 1 }, { unique: true });
db.users.createIndex({ 'username': 1 }, { unique: true });
db.users.createIndex({ 'created_at': 1 });

db.wardrobe_items.createIndex({ 'user_id': 1 });
db.wardrobe_items.createIndex({ 'category': 1 });
db.wardrobe_items.createIndex({ 'created_at': 1 });
db.wardrobe_items.createIndex({ 'name': 'text', 'description': 'text' });

db.outfits.createIndex({ 'user_id': 1 });
db.outfits.createIndex({ 'created_at': 1 });
db.outfits.createIndex({ 'name': 'text' });

db.virtual_tryons.createIndex({ 'user_id': 1 });
db.virtual_tryons.createIndex({ 'created_at': 1 });

print('Database initialized successfully!');
