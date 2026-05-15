<script>
  import { User, GraduationCap, Link } from "lucide-svelte";

  const people = [
    {
      name: "Miguel Delgado",
      linkedin: "https://www.linkedin.com/in/miguel-delgado2000/",
      major: "Electrical Engineering",
    },
    {
      name: "Francisco",
      linkedin: "https://www.linkedin.com/in/franciscoortegapantoja/",
      major: "Computer Science",
    },
  ];
</script>

<div class="flex min-h-screen items-center justify-center bg-white px-8 py-20">
  <div class="grid gap-20 md:grid-cols-2">
    {#each people as person}
      <div
        class="flex aspect-square w-72 flex-col items-center justify-center rounded-3xl border border-zinc-300 bg-white p-8 text-center shadow-sm transition hover:border-zinc-500"
      >
        <div class="mb-6 rounded-full border border-zinc-400 p-4 text-black">
          <User class="h-6 w-6" />
        </div>

        <h2 class="text-2xl font-semibold text-black">
          {person.name}
        </h2>

        <div class="mt-4 flex items-center gap-2 text-zinc-600">
          <GraduationCap class="h-4 w-4" />
          <span>{person.major}</span>
        </div>

        <a
          href={person.linkedin}
          target="_blank"
          rel="noopener noreferrer"
          class="mt-8 inline-flex items-center gap-2 text-zinc-700 transition hover:text-black"
        >
          <Link class="h-4 w-4" />
          LinkedIn
        </a>
      </div>
    {/each}
  </div>
</div>
