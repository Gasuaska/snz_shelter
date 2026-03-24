from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('database', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnimalTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TaggedAnimal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(
                    to='contenttypes.contenttype',
                    on_delete=django.db.models.deletion.CASCADE,
                )),
                ('tag', models.ForeignKey(
                    to='database.animaltag',
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='tagged_items',
                )),
            ],
        ),
    ]