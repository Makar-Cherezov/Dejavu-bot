from peewee import *
from peewee import TextField
from playhouse.shortcuts import ThreadSafeDatabaseMetadata

database = SqliteDatabase('garazhka.db', )


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = database
        model_metadata_class = ThreadSafeDatabaseMetadata


class Category(BaseModel):
    category_id = AutoField(column_name='CategoryID')
    category_name = TextField(column_name='CategoryName')

    class Meta:
        table_name = 'Category'


class Statuses(BaseModel):
    status_id = AutoField(column_name='StatusID')
    status_name = TextField(column_name='StatusName')

    class Meta:
        table_name = 'Statuses'


class Size(BaseModel):
    size_id = AutoField(column_name='SizeID')
    size_mark = TextField(column_name='SizeMark', null=True)

    class Meta:
        table_name = 'Size'


class Filters(BaseModel):
    category_key = IntegerField(column_name='Category_key', null=True)
    pricing = TextField(column_name='Pricing', null=True)
    sex_key = IntegerField(column_name='Sex_key', null=True)
    user_id = AutoField(column_name='User_id')

    class Meta:
        table_name = 'Filters'


class Clothing(BaseModel):
    category = ForeignKeyField(column_name='Category', field='category_id', model=Category)
    cloth_id = AutoField(column_name='ClothID')
    description: TextField = TextField(column_name='Description', null=True)
    name = TextField(column_name='Name')
    price = FloatField(column_name='Price')
    size = ForeignKeyField(column_name='Size', field='size_id', model=Size, null=True)
    status = ForeignKeyField(column_name='Status', field='status_id', model=Statuses)

    def GetImagePaths(self):
        query = (ImagesOfClothing.select(ImagesOfClothing.image_path)
                 .where(ImagesOfClothing.clothFK == self.cloth_id))
        image_paths = []
        for im in query:
            image_paths.append(f"./images/{im.image_path}")
        return image_paths

    class Meta:
        table_name = 'Clothing'


class ImagesOfClothing(BaseModel):
    clothFK = ForeignKeyField(column_name='ClothID', field='cloth_id', model=Clothing, null=True)
    image_path = TextField(column_name='ImagePath')
    image_id = AutoField(column_name='ClothImageID')

    class Meta:
        table_name = 'Images_of_Clothing'


class Requests(BaseModel):
    cloth = ForeignKeyField(column_name='ClothID', field='cloth_id', model=Clothing, null=True)
    date = TextField(column_name='Date')
    user_id = TextField(column_name='UserID')

    class Meta:
        table_name = 'Requests'
        indexes = (
            (('cloth', 'user_id'), True),
        )
        primary_key = CompositeKey('cloth', 'user_id')


class Sex(BaseModel):
    sex_id = AutoField(column_name='SexID')
    sex_name = TextField(column_name='SexName')

    class Meta:
        table_name = 'Sex'


class SqliteSequence(BaseModel):
    name = BareField(null=True)
    seq = BareField(null=True)

    class Meta:
        table_name = 'sqlite_sequence'
        primary_key = False


'''cursor = conn.cursor()
cursor.execute("SELECT CategoryName FROM Category ORDER BY CategoryName")
results = cursor.fetchall()
print(results)
conn.close()'''
