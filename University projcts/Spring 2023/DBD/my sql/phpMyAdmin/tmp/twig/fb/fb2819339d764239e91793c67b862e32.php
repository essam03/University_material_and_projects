<?php

use Twig\Environment;
use Twig\Error\LoaderError;
use Twig\Error\RuntimeError;
use Twig\Extension\SandboxExtension;
use Twig\Markup;
use Twig\Sandbox\SecurityError;
use Twig\Sandbox\SecurityNotAllowedTagError;
use Twig\Sandbox\SecurityNotAllowedFilterError;
use Twig\Sandbox\SecurityNotAllowedFunctionError;
use Twig\Source;
use Twig\Template;

/* database/routines/execute_form.twig */
class __TwigTemplate_2fa063a6cd113a6f521540cf7d7c335f extends Template
{
    private $source;
    private $macros = [];

    public function __construct(Environment $env)
    {
        parent::__construct($env);

        $this->source = $this->getSourceContext();

        $this->parent = false;

        $this->blocks = [
        ];
    }

    protected function doDisplay(array $context, array $blocks = [])
    {
        $macros = $this->macros;
        // line 1
        echo "<form action=\"";
        echo PhpMyAdmin\Url::getFromRoute("/database/routines");
        echo "\" method=\"post\" class=\"rte_form ajax\" onsubmit=\"return false\">
  <input type=\"hidden\" name=\"item_name\" value=\"";
        // line 2
        echo twig_escape_filter($this->env, (($__internal_compile_0 = ($context["routine"] ?? null)) && is_array($__internal_compile_0) || $__internal_compile_0 instanceof ArrayAccess ? ($__internal_compile_0["item_name"] ?? null) : null), "html", null, true);
        echo "\">
  <input type=\"hidden\" name=\"item_type\" value=\"";
        // line 3
        echo twig_escape_filter($this->env, (($__internal_compile_1 = ($context["routine"] ?? null)) && is_array($__internal_compile_1) || $__internal_compile_1 instanceof ArrayAccess ? ($__internal_compile_1["item_type"] ?? null) : null), "html", null, true);
        echo "\">
  ";
        // line 4
        echo PhpMyAdmin\Url::getHiddenInputs(($context["db"] ?? null));
        echo "

  <div class=\"card\">
    <div class=\"card-header\">";
        // line 7
        echo twig_escape_filter($this->env, ((($context["ajax"] ?? null)) ? (_gettext("Routine parameters")) : ((($__internal_compile_2 = ($context["routine"] ?? null)) && is_array($__internal_compile_2) || $__internal_compile_2 instanceof ArrayAccess ? ($__internal_compile_2["item_name"] ?? null) : null))), "html", null, true);
        echo "</div>

    <div class=\"card-body\">
      <table class=\"table w-auto rte_table";
        // line 10
        echo (( !($context["ajax"] ?? null)) ? (" caption-top") : (""));
        echo "\">
        ";
        // line 11
        if ( !($context["ajax"] ?? null)) {
            // line 12
            echo "          <caption class=\"tblHeaders\">";
echo _gettext("Routine parameters");
            echo "</caption>
        ";
        }
        // line 14
        echo "        <tr>
          <th>";
echo _gettext("Name");
        // line 15
        echo "</th>
          <th>";
echo _gettext("Type");
        // line 16
        echo "</th>
          ";
        // line 17
        if (($context["show_function_fields"] ?? null)) {
            // line 18
            echo "            <th>";
echo _gettext("Function");
            echo "</th>
          ";
        }
        // line 20
        echo "          <th>";
echo _gettext("Value");
        echo "</th>
        </tr>
        ";
        // line 22
        $context['_parent'] = $context;
        $context['_seq'] = twig_ensure_traversable(range(0, ((($__internal_compile_3 = ($context["routine"] ?? null)) && is_array($__internal_compile_3) || $__internal_compile_3 instanceof ArrayAccess ? ($__internal_compile_3["item_num_params"] ?? null) : null) - 1)));
        $context['loop'] = [
          'parent' => $context['_parent'],
          'index0' => 0,
          'index'  => 1,
          'first'  => true,
        ];
        if (is_array($context['_seq']) || (is_object($context['_seq']) && $context['_seq'] instanceof \Countable)) {
            $length = count($context['_seq']);
            $context['loop']['revindex0'] = $length - 1;
            $context['loop']['revindex'] = $length;
            $context['loop']['length'] = $length;
            $context['loop']['last'] = 1 === $length;
        }
        foreach ($context['_seq'] as $context["_key"] => $context["i"]) {
            // line 23
            echo "          <tr>
            <td>";
            // line 24
            echo twig_escape_filter($this->env, (($__internal_compile_4 = (($__internal_compile_5 = ($context["routine"] ?? null)) && is_array($__internal_compile_5) || $__internal_compile_5 instanceof ArrayAccess ? ($__internal_compile_5["item_param_name"] ?? null) : null)) && is_array($__internal_compile_4) || $__internal_compile_4 instanceof ArrayAccess ? ($__internal_compile_4[twig_get_attribute($this->env, $this->source, $context["loop"], "index0", [], "any", false, false, false, 24)] ?? null) : null), "html", null, true);
            echo "</td>
            <td>";
            // line 25
            echo twig_escape_filter($this->env, (($__internal_compile_6 = (($__internal_compile_7 = ($context["routine"] ?? null)) && is_array($__internal_compile_7) || $__internal_compile_7 instanceof ArrayAccess ? ($__internal_compile_7["item_param_type"] ?? null) : null)) && is_array($__internal_compile_6) || $__internal_compile_6 instanceof ArrayAccess ? ($__internal_compile_6[twig_get_attribute($this->env, $this->source, $context["loop"], "index0", [], "any", false, false, false, 25)] ?? null) : null), "html", null, true);
            echo "</td>
            ";
            // line 26
            if (($context["show_function_fields"] ?? null)) {
                // line 27
                echo "              <td>
                ";
                // line 28
                if ( !(null === (($__internal_compile_8 = (($__internal_compile_9 = ($context["params"] ?? null)) && is_array($__internal_compile_9) || $__internal_compile_9 instanceof ArrayAccess ? ($__internal_compile_9[twig_get_attribute($this->env, $this->source, $context["loop"], "index0", [], "any", false, false, false, 28)] ?? null) : null)) && is_array($__internal_compile_8) || $__internal_compile_8 instanceof ArrayAccess ? ($__internal_compile_8["generator"] ?? null) : null))) {
                    // line 29
                    echo "                  <select name=\"funcs[";
                    echo twig_escape_filter($this->env, (($__internal_compile_10 = (($__internal_compile_11 = ($context["routine"] ?? null)) && is_array($__internal_compile_11) || $__internal_compile_11 instanceof ArrayAccess ? ($__internal_compile_11["item_param_name"] ?? null) : null)) && is_array($__internal_compile_10) || $__internal_compile_10 instanceof ArrayAccess ? ($__internal_compile_10[twig_get_attribute($this->env, $this->source, $context["loop"], "index0", [], "any", false, false, false, 29)] ?? null) : null), "html", null, true);
                    echo "]\">
                    ";
                    // line 30
                    echo (($__internal_compile_12 = (($__internal_compile_13 = ($context["params"] ?? null)) && is_array($__internal_compile_13) || $__internal_compile_13 instanceof ArrayAccess ? ($__internal_compile_13[twig_get_attribute($this->env, $this->source, $context["loop"], "index0", [], "any", false, false, false, 30)] ?? null) : null)) && is_array($__internal_compile_12) || $__internal_compile_12 instanceof ArrayAccess ? ($__internal_compile_12["generator"] ?? null) : null);
                    echo "</select>
                ";
                } else {
                    // line 32
                    echo "                  --
                ";
                }
                // line 34
                echo "              </td>
            ";
            }
            // line 36
            echo "            <td class=\"nowrap\">
              ";
            // line 37
            if (twig_in_filter((($__internal_compile_14 = (($__internal_compile_15 = ($context["routine"] ?? null)) && is_array($__internal_compile_15) || $__internal_compile_15 instanceof ArrayAccess ? ($__internal_compile_15["item_param_type"] ?? null) : null)) && is_array($__internal_compile_14) || $__internal_compile_14 instanceof ArrayAccess ? ($__internal_compile_14[twig_get_attribute($this->env, $this->source, $context["loop"], "index0", [], "any", false, false, false, 37)] ?? null) : null), [0 => "ENUM", 1 => "SET"])) {
                // line 38
                echo "                ";
                $context['_parent'] = $context;
                $context['_seq'] = twig_ensure_traversable((($__internal_compile_16 = (($__internal_compile_17 = ($context["routine"] ?? null)) && is_array($__internal_compile_17) || $__internal_compile_17 instanceof ArrayAccess ? ($__internal_compile_17["item_param_length_arr"] ?? null) : null)) && is_array($__internal_compile_16) || $__internal_compile_16 instanceof ArrayAccess ? ($__internal_compile_16[twig_get_attribute($this->env, $this->source, $context["loop"], "index0", [], "any", false, false, false, 38)] ?? null) : null));
                $context['loop'] = [
                  'parent' => $context['_parent'],
                  'index0' => 0,
                  'index'  => 1,
                  'first'  => true,
                ];
                if (is_array($context['_seq']) || (is_object($context['_seq']) && $context['_seq'] instanceof \Countable)) {
                    $length = count($context['_seq']);
                    $context['loop']['revindex0'] = $length - 1;
                    $context['loop']['revindex'] = $length;
                    $context['loop']['length'] = $length;
                    $context['loop']['last'] = 1 === $length;
                }
                foreach ($context['_seq'] as $context["_key"] => $context["value"]) {
                    // line 39
                    echo "                  <input name=\"params[";
                    echo twig_escape_filter($this->env, (($__internal_compile_18 = (($__internal_compile_19 = ($context["routine"] ?? null)) && is_array($__internal_compile_19) || $__internal_compile_19 instanceof ArrayAccess ? ($__internal_compile_19["item_param_name"] ?? null) : null)) && is_array($__internal_compile_18) || $__internal_compile_18 instanceof ArrayAccess ? ($__internal_compile_18[twig_get_attribute($this->env, $this->source, twig_get_attribute($this->env, $this->source, twig_get_attribute($this->env, $this->source, $context["loop"], "parent", [], "any", false, false, false, 39), "loop", [], "any", false, false, false, 39), "index0", [], "any", false, false, false, 39)] ?? null) : null), "html", null, true);
                    echo "][]\" value=\"";
                    echo twig_escape_filter($this->env, (($__internal_compile_20 = (($__internal_compile_21 = (($__internal_compile_22 = ($context["params"] ?? null)) && is_array($__internal_compile_22) || $__internal_compile_22 instanceof ArrayAccess ? ($__internal_compile_22[twig_get_attribute($this->env, $this->source, twig_get_attribute($this->env, $this->source, twig_get_attribute($this->env, $this->source, $context["loop"], "parent", [], "any", false, false, false, 39), "loop", [], "any", false, false, false, 39), "index0", [], "any", false, false, false, 39)] ?? null) : null)) && is_array($__internal_compile_21) || $__internal_compile_21 instanceof ArrayAccess ? ($__internal_compile_21["htmlentities"] ?? null) : null)) && is_array($__internal_compile_20) || $__internal_compile_20 instanceof ArrayAccess ? ($__internal_compile_20[twig_get_attribute($this->env, $this->source, $context["loop"], "index0", [], "any", false, false, false, 39)] ?? null) : null), "html", null, true);
                    echo "\" type=\"";
                    echo twig_escape_filter($this->env, (($__internal_compile_23 = (($__internal_compile_24 = ($context["params"] ?? null)) && is_array($__internal_compile_24) || $__internal_compile_24 instanceof ArrayAccess ? ($__internal_compile_24[twig_get_attribute($this->env, $this->source, twig_get_attribute($this->env, $this->source, twig_get_attribute($this->env, $this->source, $context["loop"], "parent", [], "any", false, false, false, 39), "loop", [], "any", false, false, false, 39), "index0", [], "any", false, false, false, 39)] ?? null) : null)) && is_array($__internal_compile_23) || $__internal_compile_23 instanceof ArrayAccess ? ($__internal_compile_23["input_type"] ?? null) : null), "html", null, true);
                    echo "\">
                  ";
                    // line 40
                    echo twig_escape_filter($this->env, (($__internal_compile_25 = (($__internal_compile_26 = (($__internal_compile_27 = ($context["params"] ?? null)) && is_array($__internal_compile_27) || $__internal_compile_27 instanceof ArrayAccess ? ($__internal_compile_27[twig_get_attribute($this->env, $this->source, twig_get_attribute($this->env, $this->source, twig_get_attribute($this->env, $this->source, $context["loop"], "parent", [], "any", false, false, false, 40), "loop", [], "any", false, false, false, 40), "index0", [], "any", false, false, false, 40)] ?? null) : null)) && is_array($__internal_compile_26) || $__internal_compile_26 instanceof ArrayAccess ? ($__internal_compile_26["htmlentities"] ?? null) : null)) && is_array($__internal_compile_25) || $__internal_compile_25 instanceof ArrayAccess ? ($__internal_compile_25[twig_get_attribute($this->env, $this->source, $context["loop"], "index0", [], "any", false, false, false, 40)] ?? null) : null), "html", null, true);
                    echo "
                  <br>
                ";
                    ++$context['loop']['index0'];
                    ++$context['loop']['index'];
                    $context['loop']['first'] = false;
                    if (isset($context['loop']['length'])) {
                        --$context['loop']['revindex0'];
                        --$context['loop']['revindex'];
                        $context['loop']['last'] = 0 === $context['loop']['revindex0'];
                    }
                }
                $_parent = $context['_parent'];
                unset($context['_seq'], $context['_iterated'], $context['_key'], $context['value'], $context['_parent'], $context['loop']);
                $context = array_intersect_key($context, $_parent) + $_parent;
                // line 43
                echo "              ";
            } elseif (twig_in_filter(twig_lower_filter($this->env, (($__internal_compile_28 = (($__internal_compile_29 = ($context["routine"] ?? null)) && is_array($__internal_compile_29) || $__internal_compile_29 instanceof ArrayAccess ? ($__internal_compile_29["item_param_type"] ?? null) : null)) && is_array($__internal_compile_28) || $__internal_compile_28 instanceof ArrayAccess ? ($__internal_compile_28[twig_get_attribute($this->env, $this->source, $context["loop"], "index0", [], "any", false, false, false, 43)] ?? null) : null)), (($__internal_compile_30 = ($context["params"] ?? null)) && is_array($__internal_compile_30) || $__internal_compile_30 instanceof ArrayAccess ? ($__internal_compile_30["no_support_types"] ?? null) : null))) {
                // line 44
                echo "              ";
            } else {
                // line 45
                echo "                <input class=\"";
                echo twig_escape_filter($this->env, (($__internal_compile_31 = (($__internal_compile_32 = ($context["params"] ?? null)) && is_array($__internal_compile_32) || $__internal_compile_32 instanceof ArrayAccess ? ($__internal_compile_32[twig_get_attribute($this->env, $this->source, $context["loop"], "index0", [], "any", false, false, false, 45)] ?? null) : null)) && is_array($__internal_compile_31) || $__internal_compile_31 instanceof ArrayAccess ? ($__internal_compile_31["class"] ?? null) : null), "html", null, true);
                echo "\" type=\"text\" name=\"params[";
                echo twig_escape_filter($this->env, (($__internal_compile_33 = (($__internal_compile_34 = ($context["routine"] ?? null)) && is_array($__internal_compile_34) || $__internal_compile_34 instanceof ArrayAccess ? ($__internal_compile_34["item_param_name"] ?? null) : null)) && is_array($__internal_compile_33) || $__internal_compile_33 instanceof ArrayAccess ? ($__internal_compile_33[twig_get_attribute($this->env, $this->source, $context["loop"], "index0", [], "any", false, false, false, 45)] ?? null) : null), "html", null, true);
                echo "]\">
              ";
            }
            // line 47
            echo "            </td>
          </tr>
        ";
            ++$context['loop']['index0'];
            ++$context['loop']['index'];
            $context['loop']['first'] = false;
            if (isset($context['loop']['length'])) {
                --$context['loop']['revindex0'];
                --$context['loop']['revindex'];
                $context['loop']['last'] = 0 === $context['loop']['revindex0'];
            }
        }
        $_parent = $context['_parent'];
        unset($context['_seq'], $context['_iterated'], $context['_key'], $context['i'], $context['_parent'], $context['loop']);
        $context = array_intersect_key($context, $_parent) + $_parent;
        // line 50
        echo "      </table>
    </div>

    ";
        // line 53
        if ( !($context["ajax"] ?? null)) {
            // line 54
            echo "      <div class=\"card-footer\">
        <input class=\"btn btn-primary\" type=\"submit\" name=\"execute_routine\" value=\"";
echo _gettext("Go");
            // line 55
            echo "\">
      </div>
    ";
        } else {
            // line 58
            echo "      <input type=\"hidden\" name=\"execute_routine\" value=\"true\">
      <input type=\"hidden\" name=\"ajax_request\" value=\"true\">
    ";
        }
        // line 61
        echo "  </div>
</form>
";
    }

    public function getTemplateName()
    {
        return "database/routines/execute_form.twig";
    }

    public function isTraitable()
    {
        return false;
    }

    public function getDebugInfo()
    {
        return array (  252 => 61,  247 => 58,  242 => 55,  238 => 54,  236 => 53,  231 => 50,  215 => 47,  207 => 45,  204 => 44,  201 => 43,  184 => 40,  175 => 39,  157 => 38,  155 => 37,  152 => 36,  148 => 34,  144 => 32,  139 => 30,  134 => 29,  132 => 28,  129 => 27,  127 => 26,  123 => 25,  119 => 24,  116 => 23,  99 => 22,  93 => 20,  87 => 18,  85 => 17,  82 => 16,  78 => 15,  74 => 14,  68 => 12,  66 => 11,  62 => 10,  56 => 7,  50 => 4,  46 => 3,  42 => 2,  37 => 1,);
    }

    public function getSourceContext()
    {
        return new Source("", "database/routines/execute_form.twig", "D:\\Univercity\\DBD\\my sql\\phpMyAdmin\\templates\\database\\routines\\execute_form.twig");
    }
}
