{{ objname | escape | underline}}

.. _{{ objname }}:

.. currentmodule:: {{ module }}

.. autoclass:: {{ objname }}
   :members:
   :inherited-members:
   :no-special-members:

   {% block methods %}
   {% if methods %}

   .. rubric:: {{ _('Methods') }}

   .. autosummary::

      {% for item in methods %}
         {{ name | trim }}.{{ item | trim }}
      {% endfor %}

   {% endif %}
   {% endblock %}

   {% block attributes %}
   {% if attributes %}

   .. rubric:: {{ _('Attributes') }}

   .. autosummary::

      {% for item in attributes %}
         ~{{ name | trim }}.{{ item | trim }}
      {% endfor %}

   {% endif %}
   {% endblock %}
